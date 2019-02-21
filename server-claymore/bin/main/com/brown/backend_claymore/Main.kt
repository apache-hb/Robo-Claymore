package com.brown.backend_claymore

import io.ktor.application.*
import io.ktor.http.*
import io.ktor.response.*
import io.ktor.routing.*
import io.ktor.server.engine.*
import io.ktor.server.netty.*
import io.ktor.features.*
import io.ktor.content.TextContent

import java.io.File

import kotlinx.serialization.*
import kotlinx.serialization.json.Json

@Serializable
data class Quote(val id: Int, val text: String)

fun read(name: String): String = File(name).readText(Charsets.UTF_8)

const val serverPort = 8000

fun main(args: Array<String>) {	
	//the server is silent by default so use this to make sure the thing is running
	println("Running...")
	
	
	//read in bot info from json file the bot made
	val info = read("../bot-claymore/store/info.json")
		.replace("\n", "") //newlines are pointless
		.replace(" ", "") //spaces are also pointless


	val server = embeddedServer(Netty, port = serverPort) {
		println("Here")
		install(CORS)
		
		install(DefaultHeaders) {
			header("Access-Control-Allow-Origin", "*")
			header("Access-Control-Allow-Credentials", "true")
			header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
			header("Access-Control-Allow-Headers", "Content-Type")
		}

		routing {
			//return the bots basic info (name, id, discriminator)
			get("/info") {
				println("/info $info")
				var resp = TextContent(info, ContentType.Application.Json)
				//resp.headers = headersOf("Content-Type", "application/json");
				call.respond(resp)
			}
		}
	}

	server.start(wait = true)
}

fun Application.basicAuth() {
	println("Auth")
	
	//install(CallLogging)
	//install(ConditionalHeaders)
	//install(Routing)
}

//fun Application.main() {
	//install(CORS) 
//}