package claypi

import kotlinx.serialization.*
import kotlinx.serialization.json.*

import java.io.File

data class Prefix(
    val id: Long,
    val prefix: String
)

@Serializable
data class BotInfo(
    val name: String,
    val id: Long,
    val dis: String,
    val avatar: String
)

fun loadInfo(path: String) = Json.parse(BotInfo.serializer(), File(path).readText())
//fun loadConfig(path: String) = JsonObject(File(path).readText())