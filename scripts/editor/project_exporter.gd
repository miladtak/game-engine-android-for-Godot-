extends Node
class_name ProjectExporter

# ذخیره‌سازی داده‌های صحنه روی پوشه مشخص شده در حافظه دستگاه
func export_project_to_storage(project_path: String, scene_data: Dictionary) -> bool:
	if not DirAccess.dir_exists_absolute(project_path):
		var err = DirAccess.make_dir_recursive_absolute(project_path)
		if err != OK:
			print("خطا در ایجاد پوشه پروژه: ", err)
			return false
	
	var file_path = project_path + "project_data.json"
	var file = FileAccess.open(file_path, FileAccess.WRITE)
	if file != null:
		var json_string = JSON.stringify(scene_data, "\t")
		file.store_string(json_string)
		file.close()
		print("پروژه با موفقیت ذخیره شد: ", file_path)
		return true
	else:
		print("خطا در باز کردن فایل ذخیره! کد خطا: ", FileAccess.get_open_error())
		return false
