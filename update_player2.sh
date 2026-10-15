sed -i '/val status: String = "Active"/i \
    val isLoanedOut: Boolean = false,\
    val isLoanedIn: Boolean = false,\
    val isRegen: Boolean = false,' app/src/main/java/com/example/MainViewModel.kt
