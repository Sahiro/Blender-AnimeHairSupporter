import bpy, mathutils

class ahs_tapercurve_move(bpy.types.Operator):
	bl_idname = 'object.ahs_tapercurve_move'
	bl_label = "位置を再設定"
	bl_options = {'REGISTER', 'UNDO'}
	
	is_bevel = bpy.props.BoolProperty(name="ベベル")
	
	@classmethod
	def poll(cls, context):
		try:
			taper_and_bevel_objects = [c.taper_object for c in context.blend_data.curves if c.taper_object] + [c.bevel_object for c in context.blend_data.curves if c.bevel_object]
			for ob in context.selected_objects:
				if ob in taper_and_bevel_objects: break
			else: return False
		except: return False
		return True
	
	def execute(self, context):
		if not self.is_bevel: taper_or_bevel_objects = [c.taper_object for c in context.blend_data.curves if c.taper_object]
		else: taper_or_bevel_objects = [c.bevel_object for c in context.blend_data.curves if c.bevel_object]
		
		target_zips = []
		for ob in context.selected_objects:
			if ob.type != 'CURVE': continue
			if ob not in taper_or_bevel_objects: continue
			
			parent_ob = None
			for o in context.blend_data.objects:
				if o.type != 'CURVE': continue
				
				if not self.is_bevel and o.data.taper_object == ob: parent_ob = o
				elif self.is_bevel and o.data.bevel_object == ob: parent_ob = o
			if not parent_ob: continue
			
			target_zips.append((ob, parent_ob))
		
		for ob, parent_ob in target_zips:
			if not len(parent_ob.data.splines): continue
			end_co = parent_ob.matrix_world * mathutils.Vector(parent_ob.data.splines[0].points[-1].co[:3])
			ob.location = end_co.copy()
		
		return {'FINISHED'}
