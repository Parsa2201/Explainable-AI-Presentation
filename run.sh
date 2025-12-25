#!/bin/bash

install() {
    pip install -r requirements.txt "$@"
}

render() {
    manim-slides render Presentation.py Presentation "$@"
}

show() {
    manim-slides Presentation "$@"
}

show_html() {
    manim-slides convert Presentation slides.html --open "$@"
}

slides_config() {
    manim-slides wizard "$@"
}

render_show() {
    render
    show
}

render_show_html() {
    render
    show_html
}

cmd="$1"
shift   # remove the flag, leave the rest in "$@"

case "$cmd" in
    --install)
        install "$@"
        ;;
    --render)
        render "$@"
        ;;
    --show)
        show "$@"
        ;;
    --show-html)
        show_html "$@"
        ;;
    --slides-config)
        slides_config "$@"
        ;;
    --render-show)
        render_show "$@"
        ;;
    --render-show-html)
        render_show_html "$@"
        ;;
    *)
        echo "Unknown option: $cmd"
        exit 1
        ;;
esac