const $timer = $("#timer")
const $form = $("#submit-form :input")
const $btnNewGame = $("#new-game")
function startTimer(){
    let currTime = parseInt($timer.html())
    $btnNewGame.hide()
    let interval = setInterval(() => {
            currTime -= 1
            console.log(currTime)
            $timer.html(currTime)
            if (currTime == 0) {
                clearInterval(interval)
            }
        }, 1000);
    interval
}

function endTimer(){
    let currTime = parseInt($timer.html())
    setTimeout(async function () {
        $form.prop("disabled", true)
        endGame()
        const stats = await updateStats()
        updateStatsHtml(stats)
        $btnNewGame.show()
    }, currTime * 1000)
}

async function startUp(){
    const currStats = await getStats()
    updateStatsHtml(currStats)
}

startUp()
startTimer()
endTimer()
