package com.chudy.jpwplab3.activity

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.LinearLayout
import androidx.recyclerview.widget.LinearLayoutManager
import com.chudy.jpwplab3.R
import com.chudy.jpwplab3.adapter.QuizAdapter
import com.chudy.jpwplab3.networking.Api
import com.chudy.jpwplab3.networking.networkModule
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.coroutines.runBlocking
import okhttp3.OkHttpClient
import org.koin.android.ext.android.inject
import org.koin.core.context.startKoin
import retrofit2.Retrofit

class MainActivity : AppCompatActivity() {
    private val api: Api by inject()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        runBlocking {
            showQuiz()
        }
    }
    //TODO 1: uzupełnić metodę w dwóch miejscach, żeby otrzymywać odpowiedź z serwera,
    // przekazać ją później do adaptera.
    private suspend fun showQuiz(){
        val response = api.requestQuiz()
        recycler_main.apply{
            layoutManager = LinearLayoutManager(applicationContext)
            adapter = QuizAdapter(response)
        }
    }
}
