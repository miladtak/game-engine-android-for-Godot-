extends GraphEdit

func _ready() -> void:
	# تنظیمات گراف
	right_disconnects = true
	connection_request.connect(_on_connection_request)
	
	# ساخت چند بلوک تستی شبیه عکس
	_create_node("On_Start", Vector2(40, 40), Color(0.2, 0.5, 0.8), ["Flow Out"])
	_create_node("Variable: Player_Object", Vector2(80, 120), Color(0.3, 0.4, 0.7), ["Flow In", "Flow Out"])
	_create_node("Get_Item", Vector2(40, 300), Color(0.4, 0.5, 0.9), ["Flow In", "تعداد آیتم Out"])

func _create_node(title: String, pos: Vector2, color: Color, slots: Array) -> void:
	var node = GraphNode.new()
	node.title = title
	node.position_offset = pos
	
	# ساخت پورت‌های ورودی و خروجی برای سیم‌کشی
	var idx = 0
	for slot_name in slots:
		var lbl = Label.new()
		lbl.text = slot_name
		node.add_child(lbl)
		var is_in = slot_name.contains("In")
		var is_out = slot_name.contains("Out")
		node.set_slot(idx, is_in, 0, color, is_out, 0, color)
		idx += 1
		
	add_child(node)

func _on_connection_request(from_node: String, from_port: int, to_node: String, to_port: int) -> void:
	connect_node(from_node, from_port, to_node, to_port)
