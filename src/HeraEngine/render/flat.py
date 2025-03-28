from HeraEngine.types.Vec2 import Vec2
from HeraEngine.types.Font import Font

from HeraEngine.childs.Entity import Entity
import numpy as np

class FlatRenderer():
    def __init__(self,core):
        self.core = core

    

    def render(self, size: Vec2,target:Vec2, buffer, entityList: list[Entity], z: int):
        buffer_np = np.frombuffer(buffer, dtype=np.uint32).reshape(size.y, size.x)
       
        
        for entity in entityList:
            if not isinstance(entity, Entity):
                raise TypeError(f"Target is not an Entity (type: {type(entity).__name__})")
            
            pos = entity.position
            ent_size = entity.size

            if entity.is_text == True:
                self.render_text(entity, buffer_np, z, size, pos)
                continue
            
            if entity.textured:
                self.render_textured(entity, buffer_np, z, size, pos, ent_size)
                continue
                
            self.render_square(buffer_np, z, size, pos, ent_size, entity.color.value)

        return buffer

    def render_text(self, entity, buffer_np, z, size, pos):
        font = entity.font
        if not isinstance(font,Font):
            raise TypeError("Entity doesn't have valid Font.")
        
        font_size = font.size
        offset = 0
        y_offset = 0

        for i in entity.text:
            if i == "ٲ":
                offset = 0
                y_offset += font.size.y
                continue
            texture_data = font.get_char(i).data
        
            buf_y_start, buf_y_end = np.clip([pos.y+ font.offset.y + y_offset, pos.y + font_size.y + font.offset.y + y_offset], 0, size.y)
            buf_x_start, buf_x_end = np.clip([pos.x + offset, pos.x + font_size.x + offset], 0, size.x)
    
            small_y_start = max(0, -pos.y)
            small_y_end = small_y_start + (buf_y_end - buf_y_start)
            small_x_start = max(0, -pos.x)
            small_x_end = small_x_start + (buf_x_end - buf_x_start)

            buffer_view = buffer_np[buf_y_start:buf_y_end, buf_x_start:buf_x_end]
            texture_patch = texture_data[small_y_start:small_y_end, small_x_start:small_x_end]

            non_zero_mask = texture_patch != 0
            np.copyto(buffer_view, texture_patch, where=non_zero_mask)
            offset += font_size.x
            offset += font.offset.x

    def render_textured(self, entity, buffer_np, z, size, pos, ent_size):
        texture_data = entity.texture.data
        rotation = int(getattr(entity, 'rotation', 0)*10)/10
        new_pos = Vec2(pos.x,pos.y)
        if rotation != 0:
            original_center_x = pos.x + ent_size.x / 2
            original_center_y = pos.y + ent_size.y / 2

            possible_chache = entity.texture.get_rotation(rotation)
            if possible_chache != None:
                texture_data, new_ent_size = possible_chache
            else:
                texture_data, new_ent_size = self.rotate_image(texture_data, rotation)
                entity.texture.store_rotation(rotation,(texture_data,new_ent_size))

  

            new_pos_x = original_center_x - new_ent_size.x / 2
            new_pos_y = original_center_y - new_ent_size.y / 2

            new_pos.x = int(new_pos_x) #No idea why but updating the position on moving entities created a bug and moves out the entities in a weird diagonal manner, gonna drop that for now
            new_pos.y = int(new_pos_y) #Fixed the bug, changing the entity position with pos.x =... offseted the entity a bit and caused a chain reaction.
            ent_size = new_ent_size

        buf_y_start, buf_y_end = np.clip([new_pos.y, new_pos.y + ent_size.y], 0, size.y)
        buf_x_start, buf_x_end = np.clip([new_pos.x, new_pos.x + ent_size.x], 0, size.x)

        small_y_start = max(0, -new_pos.y)
        small_y_end = small_y_start + (buf_y_end - buf_y_start)
        small_x_start = max(0, -new_pos.x)
        small_x_end = small_x_start + (buf_x_end - buf_x_start)

        texture_patch = texture_data[small_y_start:small_y_end, small_x_start:small_x_end]

        buffer_view = buffer_np[buf_y_start:buf_y_end, buf_x_start:buf_x_end]

        non_zero_mask = texture_patch != 0

        np.copyto(buffer_view, texture_patch, where=non_zero_mask)



    def rotate_image(self, image, angle):
        angle_rad = np.deg2rad(angle)
        cos_a = np.cos(angle_rad)
        sin_a = np.sin(angle_rad)

        h, w = image.shape
        
        new_w = int(np.ceil(w * abs(cos_a) + h * abs(sin_a)))
        new_h = int(np.ceil(h * abs(cos_a) + w * abs(sin_a)))
        
        rotated = np.zeros((new_h, new_w), dtype=image.dtype)
        
        orig_cx, orig_cy = w / 2.0, h / 2.0
        new_cx, new_cy = new_w / 2.0, new_h / 2.0
        
        Y, X = np.indices((new_h, new_w))

        Xc = X - new_cx
        Yc = Y - new_cy

        Xs = cos_a * Xc + sin_a * Yc
        Ys = -sin_a * Xc + cos_a * Yc

        Xs += orig_cx
        Ys += orig_cy
        
        Xs_int = np.rint(Xs).astype(int)
        Ys_int = np.rint(Ys).astype(int)

        valid = (Xs_int >= 0) & (Xs_int < w) & (Ys_int >= 0) & (Ys_int < h)
        
        rotated[valid] = image[Ys_int[valid], Xs_int[valid]]
        
        return rotated, Vec2(new_w, new_h)

    def render_square(self, buffer_np, z, size, pos, ent_size, color):
        y_start, y_end = np.clip([pos.y, pos.y + ent_size.y], 0, size.y)
        x_start, x_end = np.clip([pos.x, pos.x + ent_size.x], 0, size.x)
        
        if y_start >= y_end or x_start >= x_end:
            return

        buffer_slice = buffer_np[y_start:y_end, x_start:x_end]
        buffer_slice[:] = color

