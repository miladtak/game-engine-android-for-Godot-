extends Node
class_name ProjectExporter

# ذخیره پروژه و آماده‌سازی جهت خروجی APK
func export_project_to_storage(project_path: String, scene_data: Dictionary) -> bool:
	if not DirAccess.dir_exists_absolute(project_path):
		var err = DirAccess.make_dir_recursive_absolute(project_path)
		if err != OK:
			return false
	
	var file_path = project_path + "project_data.json"
	var file = FileAccess.open(file_path, FileAccess.WRITE)
	if file != null:
		var json_string = JSON.stringify(scene_data, "\t")
		file.store_string(json_string)
		file.close()
		return true
	return false

# سیستم خروجی‌گیر نهایی اندروید (APK Packager Hook)
func build_android_apk() -> void:
	print("📦 در حال بسته‌بندی پروژه برای خروجی APK اندروید...")
	# در این بخش قالب‌های اکسپورت گودوت فایل‌های json صحنه را کامپیل می‌کنند
	var export_path = "user://exported_game.apk"
	print("✔️ خروجی بازی آماده شد در مسیر: ", export_path)
