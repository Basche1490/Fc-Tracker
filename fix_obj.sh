sed -i 's/ClubObjective/Objective/g' app/src/main/java/com/example/ui/screens/SeasonSummaryScreen.kt
sed -i 's/obj.isCompleted/obj.status == "Completed"/g' app/src/main/java/com/example/ui/screens/SeasonSummaryScreen.kt
sed -i 's/isCompleted = !obj.status == "Completed"/status = if (obj.status == "Completed") "In Progress" else "Completed"/g' app/src/main/java/com/example/ui/screens/SeasonSummaryScreen.kt
sed -i 's/isCompleted = it/status = if (it) "Completed" else "In Progress"/g' app/src/main/java/com/example/ui/screens/SeasonSummaryScreen.kt
sed -i 's/obj.title/obj.description/g' app/src/main/java/com/example/ui/screens/SeasonSummaryScreen.kt
sed -i 's/title = objTitle/description = objTitle, category = "General"/g' app/src/main/java/com/example/ui/screens/SeasonSummaryScreen.kt
