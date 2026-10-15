sed -i '/val isAcademy: Boolean = false,/a \
    val isLoanedOut: Boolean = false,\
    val isLoanedIn: Boolean = false,\
    val isRegen: Boolean = false,\
    val isInjured: Boolean = false,\
    val fieldX: Float = -1f,\
    val fieldY: Float = -1f,' app/src/main/java/com/example/MainViewModel.kt
