extends Control

var selected_node: Node2D = null
var is_dragging: bool = false
var drag_offset: Vector2 = Vector2.ZERO

func _input(event):
	if event is InputEventScreenTouch:
		if event.pressed:
			# تشخیص لمس روی اشیا
			var touch_pos = event.position
			if selected_node and selected_node.get_rect().has_point(touch_pos):
				is_dragging = true
				drag_offset = selected_node.global_position - touch_pos
		else:
			is_dragging = false
			
	elif event is InputEventScreenDrag and is_dragging:
		if selected_node:
			selected_node.global_position = event.position + drag_offset
