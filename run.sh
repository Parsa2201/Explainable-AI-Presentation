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
    *)
        echo "Unknown option: $cmd"
        exit 1
        ;;
esac