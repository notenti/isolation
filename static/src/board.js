export default function() {
    let html = ''
    const board_height = 7
    const board_width = 7

    for (var i = 0; i < board_height; i++) {
        html += '<div class="{i}">'
        for (var j = 0; j < board_width; j++){
            html += `<div class="square" id="${i}${j}"></div>`
        }
        html += '</div>' //end row
    }

    return html
}