import Board from './board'
import $ from 'jquery'

export default class Isolation {
    constructor(dom_element) {
        const $container = checkContainerArg(dom_element)
        if (!$container) return null
        let $board = null
        let widget = {}

        widget.resize = function () {
            $board.css('width', '500px')
            $board.html(Board())
        }

        function buildContainerHTML() {
            const html = '<div class=isolation> <div class="board"></div> </div>'
            return html
        }

        function checkContainerArg(dom_element) {
            dom_element = '#' + dom_element
            const $container = $(dom_element)
            if ($container.length !== 1) {
                window.alert('Something went wrong.')
                return false
            }
            return $container
        }

        function initDOM() {
            $container.html(buildContainerHTML())
            $board = $container.find('.board')
            widget.resize()
        }

        initDOM()
        return widget
    }
}

