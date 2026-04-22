function create_gauge(gauge_id, text) {
    let container = document.createElement("div")
    container.id = `${gauge_id}-container`
    container.className = "gauge-container"

    let gauge = document.createElement("div")
    gauge.className = "gauge"
    gauge.id = gauge_id

    let gauge_background = document.createElement("div")
    gauge_background.className = "gauge-background"

    let gauge_foreground = document.createElement("div")
    gauge_foreground.className = "gauge-foreground"

    let gauge_text = document.createElement("p")
    gauge_text.innerText = text
    gauge_text.style.textAlign = "center"
    gauge_text.style.fontWeight = "bold"

    gauge_foreground.appendChild(gauge_text)

    let gauge_border = document.createElement("div")
    gauge_border.className = "gauge-border inset-shadow"

    container.appendChild(gauge)
    container.appendChild(gauge_background)
    container.appendChild(gauge_foreground)
    container.appendChild(gauge_border)

    return container
}

function update_gauge(gauge_id, new_val) {
    let gauge = document.getElementById(gauge_id)
    let angle = Math.min((new_val / 100), 1) * 180

    gauge.style.rotate = `${180 + angle}deg`
}