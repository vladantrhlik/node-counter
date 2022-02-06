import bpy
bl_info = {
    "name": "Node counter",
    "description": "Counts all nodes in active node tree",
    "author": "Vladan Trhlík (valdosh)",
    "blender": (2, 80, 0),
    "category": "Node",
}

class NC_PT_Panel(bpy.types.Panel):
    
    bl_idname = 'NODE_COUNTER_PT'
    bl_label = 'Node counter'
    bl_category = "Node counter"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    
    def __init__(self):
        self.types = {}

    def count_in_tree(self, tree):
        count = 0
        groups_counted = []
        for n in tree.nodes:
            count += 1
            # types
            if n.type not in self.types:
                self.types[n.type] = 1
            else:
                self.types[n.type] += 1
            # groups
            if n.type == 'GROUP' and n.node_tree not in groups_counted:
                groups_counted.append(n.node_tree)
                count += self.count_in_tree(n.node_tree)
                
        return count
    
    def draw(self, context):
        node_tree = bpy.context.space_data.edit_tree
        self.types = {}
        count = self.count_in_tree(node_tree)
        
        self.layout.label(text="Node tree:")
        main = self.layout.box()
        row = main.row()
        row.label(text="CURRENT")
        row.label(text=str(node_tree.name))
        
        row = main.row()
        row.label(text="COUNT")
        row.label(text=str(count))
        
        
        self.layout.label(text="Node stats:")
        stat_box = self.layout.box()
        
        for t in sorted(self.types.keys()):
            row = stat_box.row()
            row.label(text=t)
            row.label(text=str(self.types[t]))

def register():
    bpy.utils.register_class(NC_PT_Panel)

def unregister():
    bpy.utils.unregister_class(NC_PT_Panel)

if __name__ == '__main__':
    register()