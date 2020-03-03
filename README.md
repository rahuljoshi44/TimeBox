# TimeBox
<p>
TimeBox is a task management app with data analysis features, inspired by the "screen time" feature of iOS. It was created using django and the django rest framework. The UI utlizes libraries such as chart.js and boostrap.
</p> <br />
<p align="center">
  <img src="demo/intro.gif" height=400px>
</p>

## Features

TimeBox was created to allow for easy management of daily and weekly tasks.
Specifically, it can:  

### Set weekly goals

Use TimeBox to set your goals for the week. You can even add subtasks within goals to keep track of your progess.
- Set goals that expire within the week if not completed.
- Create subtasks within each goal to track your progress.
- Subtasks can be added to your daily task list to complete.
<br />
<p align="center">
  <img src="demo/goals.png" height=400px class="shadow">
</p>

### Manage daily tasks

Create and manage a list of tasks to complete in the day. You can decide how much time you are willing to spend on each task.
Additionally, tasks can be categorized by: 
- Type: whether the task is for work, fun, self development, excercise, errands, etc.
- Priority: whether it is high, medium or low priority.
<br />
<p align="center">
  <img src="demo/today.png" height=400px >
</p>

### Completed tasks

View the percentage of tasks you completed for each day over the past week. This is calculated by dividing the number of completed tasks by the number of tasks not completed.
<br />
<p align="center">
  <img src="demo/completion.png" height=400px>
</p>

### Time spent on each category

Study the different places you spend your time over the day. TimeBox groups each completed task by category and sums up all minutes you spend on them to create a graph that shows how much time was spent on each category of tasks.<br />
<p align="center">
  <img src="demo/category1.png" height=400px>
</p> <br />
You can even see how much time you spent on each category over the entire week.<br />
<p align="center">
  <img src="demo/category2.png" height=400px>
</p>

### Download Reports

Download reports as a pdf about the tasks you completed and did not complete to store and review whenever you want.
<br />
<p align="center">
  <img src="demo/reports.png" height=400px>
</p>
