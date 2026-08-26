extends Node

var current_locale: String = "fa"

func _ready() -> void:
    set_language("fa")

func set_language(lang_code: String) -> void:
    current_locale = lang_code
    TranslationServer.set_locale(lang_code)

func is_rtl() -> bool:
    return current_locale == "fa" or current_locale == "ar"
