import kotlinx.serialization.*
import kotlinx.serialization.json.Json

@Serializable
data class BotInfo(
    val name: String,
    val id: Long,
    val dis: String,
    val avatar: String
)
