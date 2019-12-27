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
import java.io.FileNotFoundException

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

fun Wini.getLong(head: String, field: String): Long? = this.get(head, field, Long::class.java)

fun String.toJsonString() = "\"$this\""
fun <T: String> List<T>.toJsonString() = this.map { it.toJsonString() }.joinToString(", ", "[", "]")

class NotFound : Exception()

const val port = 8080

suspend fun main(args: Array<String>) {
    val configPath = File("../config/config.ini")
    configPath.parentFile.mkdirs()
    configPath.createNewFile()
    val cfg = Wini(configPath)

    val mongoUrl: String? = cfg.get("mongo", "url")
    val client = if(mongoUrl != null) MongoClients.create(mongoUrl) else MongoClients.create()
    val db = client.getDatabase(cfg.get("mongo", "name"))
    val prefixes = db.getCollection("prefix")

    val defaultPrefix = cfg.get("discord", "prefix")

    val discordID = cfg.getLong("discord", "id")!!
    val discordSecret = cfg.get("discord", "secret")

    val discordCreds = Base64.encode("$discordID:$discordSecret".toByteArray())
    val redirect = URLEncoder.encode("http://localhost:$port/discord/callback", "UTF-8")
    val discordScope = URLEncoder.encode("identify guilds connections")

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
                    when(val user = discord?.selfUser) {
                        null -> throw NotFound()
                        else -> call.respondText("""{
                            "id": ${user.id},
                            "user": "${user.username}",
                            "dis": ${user.discriminator},
                            "avatar": ${user.avatar.uri}
                        }""", ContentType.Application.Json)
                    }
                }

                route("quotes") {
                    get("for") {
                        when(val id = call.parameters["id"]?.toLongOrNull()) {
                            null -> call.respondText("""{ "quotes": null }""", ContentType.Application.Json)
                            else -> call.respondText("""{ "quotes": [] }""", ContentType.Application.Json)
                        }
                    }

                    delete("delete") {

                    }
                }
            }

            route("discord") {
                get("login") {
                    call.respondRedirect("https://discordapp.com/api/oauth2/authorize?client_id=$discordID&scope=$discordScope&response_type=code&redirect_uri=$redirect")
                }
                get("callback") {
                    println("got here as well")
                    val resp = call.parameters["code"]?.let { code ->
                        httpPost {
                            scheme = "https"
                            host = "discordapp.com"
                            path = "/api/oauth2/token"

                            param {
                                "client_id" to discordID
                                "client_secret" to discordSecret
                                "grant_type" to "authorization_code"
                                "code" to code
                                "redirect_uri" to redirect
                            }

                            header {
                                "Authorization" to "Basic $discordCreds"
                                "Content-Type" to "application/x-www-url-form-urlencoded"
                            }
                        }
                    }
                    println(resp)
                    resp?.use { data ->
                        if(data.code() != 200)
                            throw NotFound()
                        println(data)
                        call.respondText("Yeet", ContentType.Text.Html)
                    }
                }
            }
        }
    }.start(wait = true)
}
