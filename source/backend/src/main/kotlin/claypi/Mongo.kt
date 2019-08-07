package claypi

import org.litote.kmongo.reactivestreams.*
import org.litote.kmongo.coroutine.*


// ths class that has the data
class DataBase(dbName: String) {
    private val client: CoroutineClient
    private val database: CoroutineDatabase
    init {
        client = KMongo.createClient().coroutine
        database = client.getDatabase(dbName)
    }

    suspend fun getPrefix(server: Long) {
        val col = database.getCollection<Prefix>()
        val dat = col.findOne(Prefix::id eq server)

        if(dat != null) {
            return dat
        } else {
            return 
        }
    }
}