package claypi

// database access
import com.mongodb.*
import com.mongodb.client.*
import com.mongodb.client.model.Filters.eq
import org.reactivestreams.Subscriber
import org.reactivestreams.Subscription
import org.bson.Document

// config parsing
import org.ini4j.*
import java.io.File

// discord api stuff
import com.serebit.strife.*

// oauth discord stuff
import org.jetbrains.hub.oauth2.client.*
import java.net.URLEncoder
import java.net.URL
import io.github.rybalkinsd.kohttp.dsl.*

// coroutines
import kotlinx.coroutines.*

// web server stuff
import io.ktor.application.*
import io.ktor.http.*
import io.ktor.response.*
import io.ktor.features.*
import io.ktor.routing.*
import io.ktor.server.engine.*
import io.ktor.server.netty.*

fun config(path: String) = Wini(File(path))

fun Wini.getInt(head: String, field: String): Int? = this.get(head, field, Int::class.java)

fun String.toJsonString(): String = "\"$this\""

class NotFound : Exception()

suspend fun main(args: Array<String>) {
    val cfg = config("../config/config.ini")

    val mongoUrl: String? = cfg.get("mongo", "url")
    val client = if(mongoUrl != null) MongoClients.create(mongoUrl) else MongoClients.create()
    val db = client.getDatabase(cfg.get("mongo", "name"))
    val prefixes = db.getCollection("prefix")

    val defaultPrefix = cfg.get("discord", "prefix")

    val discordID = cfg.getInt("oauth", "id")!!
    val discordSecret = cfg.get("oauth", "secret")

    val port = cfg.getInt("api", "port")!!
    val discordCreds = Base64.encode("$discordID:$discordSecret".toByteArray())
    val redirect = URLEncoder.encode("http://localhost:$port/api/discord/callback", "UTF-8")

    var discord: BotClient? = null

    GlobalScope.launch {
        bot(cfg.get("discord", "token")) {
            onReady {
                discord = context
                println("bot has logged in")
            }
        }
    }

    embeddedServer(Netty, port) {
        install(StatusPages) {
            exception<NotFound> { _ -> call.respond(HttpStatusCode.NotFound) }
        }
        routing {
            route("api/v1") {
                // get the prefix for a server
                get("prefix") {
                    when(val id = call.parameters["id"]?.toLongOrNull()) {
                        null -> call.respondText("""{ "prefix": null }""")
                        else -> {
                            val prefix = prefixes.find(eq("id", id)).first()?.get("prefix") as String?
                            call.respondText("""{ "prefix": ${prefix?.toJsonString()} }""", ContentType.Application.Json)
                        }
                    }
                }
                get("prefix/global") {
                    call.respondText("""{ "prefix": "$defaultPrefix" }""", ContentType.Application.Json)
                }

                get("bot") {

                }
            }

            route("discord") {
                get("login") {
                   call.respondRedirect("https://discordapp.com/api/oauth2/authorize?client_id=$discordID&scope=identify&response_type=code&redirect_uri=$redirect")
                }
                get("callback") {
                    call.parameters["code"]?.let { code ->
                        httpPost {
                            host = "https://discordapp.com"
                            path = "/api/oauth2/token"

                            param {
                                "grant_type" to "authorization_code"
                                "code" to code
                                "redirect_uri" to redirect
                            }

                            header {
                                "Authorization" to "Basic $discordCreds"
                            }
                        }
                    }?.use { data ->
                        if(data.code() != 200)
                            throw NotFound()
                    }
                }
            }
        }
    }.start(wait = true)
}
