package com.chudy.jpwplab3.adapter

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.chudy.jpwplab3.R
import com.chudy.jpwplab3.model.Quiz
import kotlinx.android.synthetic.main.item_quiz.view.*

class QuizAdapter(private val quizList: List<Quiz>) :
    RecyclerView.Adapter<QuizAdapter.QuizViewHolder>() {

    /**
     * Item count is equal to the size of adapted list.
     */
    override fun getItemCount(): Int = quizList.size

    /**
     * Creating a viewHolder, it holds an inflated layout of an item.
     */
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): QuizViewHolder =
        QuizViewHolder(
            LayoutInflater.from(parent.context).inflate(
                R.layout.item_quiz, parent, false
            )
        )

    //TODO 3: edytować tekst stałych z poniższej klasy ViewHoldera.
    // Odpowiadają one poszczególnym elementom w layoucie item_quiz.xml - należy
    // nadać im tekst poszczególnych zmiennych.

    //TODO 4: wiedząc, że data w otrzymanym zapytaniu zapisana została jako
    // "2020-05-05 10:10:24+00:00" sformatuj i wyświetl ją do postaci
    // "2020-05-05 o godzinie 10:10"
    override fun onBindViewHolder(holder: QuizViewHolder, position: Int) {
        val quiz = quizList[position]
        holder.textName.text = quiz.name
        holder.textTopLeft.text = quiz.answers[0].name
        holder.textTopRight.text = quiz.answers[1].name
        holder.textBottomLeft.text = quiz.answers[2].name
        holder.textBottomRight.text = quiz.answers[3].name

        val date = quiz.publish_at.substring(0,10)
        val time = quiz.publish_at.substring(11, 16)
        val dateString = date + " o godzinie " + time;
        holder.textDate.text = dateString
    }

    /**
     * A view holder that holds references to the inflated layout's components.
     */
    class QuizViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val textName: TextView = itemView.text_view_item_name
        val textTopLeft: TextView = itemView.text_view_top_left
        val textTopRight: TextView = itemView.text_view_top_right
        val textBottomLeft: TextView = itemView.text_view_bottom_left
        val textBottomRight: TextView = itemView.text_view_bottom_right
        val textDate: TextView = itemView.text_view_date
    }
}