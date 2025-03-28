from PIL import Image

# The same character set from your Kaboom loadFont call:
CHARS = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"

TILE_WIDTH = 48
TILE_HEIGHT = 48

def load_font(image_path, chars=CHARS, tile_width=TILE_WIDTH, tile_height=TILE_HEIGHT):
    """
    Loads the specified font image (containing a grid of glyphs),
    slices it into individual character images, and returns them in a list.
    """
    font_image = Image.open(image_path).convert("RGBA")
    image_width, image_height = font_image.size

    # Calculate how many columns and rows the font image can contain
    columns = image_width // tile_width
    rows = image_height // tile_height

    glyph_images = []
    char_index = 0

    # Loop over rows and columns to crop out each glyph
    for row in range(rows):
        for col in range(columns):
            if char_index >= len(chars):
                # We've already sliced out all needed glyphs
                break

            x = col * tile_width
            y = row * tile_height
            # Crop out a single character glyph
            glyph = font_image.crop((x, y, x + tile_width, y + tile_height))
            glyph_images.append(glyph)

            char_index += 1

        if char_index >= len(chars):
            break

    return glyph_images

def image_to_hex_list(img):
    img = img.convert("RGBA")  
    pixels = list(img.getdata())  
    hex_list = [str(img.size[0]),str(img.size[1])]

    for r, g, b, a in pixels:
        if a == 0: 
            hex_list.append(str(0))
        else:
            hex_list.append(str((r << 16) | (g << 8) | b))

    return hex_list

char_to_sanitized = {' ': 'space', '!': 'exclamation_mark', '"': 'double_quote', '#': 'hash', '$': 'dollar_sign', '%': 'percent', '&': 'ampersand', '\'': 'apostrophe', '(': 'left_paren', ')': 'right_paren', '*': 'asterisk', '+': 'plus', ',': 'comma', '-': 'hyphen', '.': 'period', '/': 'forward_slash', '0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', ':': 'colon', ';': 'semicolon', '<': 'less_than', '=': 'equals', '>': 'greater_than', '?': 'question_mark', '@': 'at_symbol', 'A': 'A_maj', 'B': 'B_maj', 'C': 'C_maj', 'D': 'D_maj', 'E': 'E_maj', 'F': 'F_maj', 'G': 'G_maj', 'H': 'H_maj', 'I': 'I_maj', 'J': 'J_maj', 'K': 'K_maj', 'L': 'L_maj', 'M': 'M_maj', 'N': 'N_maj', 'O': 'O_maj', 'P': 'P_maj', 'Q': 'Q_maj', 'R': 'R_maj', 'S': 'S_maj', 'T': 'T_maj', 'U': 'U_maj', 'V': 'V_maj', 'W': 'W_maj', 'X': 'X_maj', 'Y': 'Y_maj', 'Z': 'Z_maj', '[': 'left_bracket', '\\': 'backslash', ']': 'right_bracket', '^': 'caret', '_': 'underscore', '`': 'backtick', 'a': 'a_min', 'b': 'b_min', 'c': 'c_min', 'd': 'd_min', 'e': 'e_min', 'f': 'f_min', 'g': 'g_min', 'h': 'h_min', 'i': 'i_min', 'j': 'j_min', 'k': 'k_min', 'l': 'l_min', 'm': 'm_min', 'n': 'n_min', 'o': 'o_min', 'p': 'p_min', 'q': 'q_min', 'r': 'r_min', 's': 's_min', 't': 't_min', 'u': 'u_min', 'v': 'v_min', 'w': 'w_min', 'x': 'x_min', 'y': 'y_min', 'z': 'z_min', '{': 'left_brace', '|': 'vertical_bar', '}': 'right_brace', '~': 'tilde'}


if __name__ == "__main__":
    # Example usage
    file = "Assets/Textures/Fonts/MonogramBig/"
    glyphs = load_font("HeraEngine/tools/big.png")
    print(f"Loaded {len(glyphs)} glyph images.")


    for i in range(len(glyphs)):
        print(i,glyphs[i],CHARS[i])
        glyphs[i].save(f"{file}{char_to_sanitized[CHARS[i]]}.png")
        data = image_to_hex_list(glyphs[i])
        file_out = f"{file}{char_to_sanitized[CHARS[i]]}.raw"

        with open(file_out,"w") as thign:
            print(file_out)
            thign.write(str(";".join(data)))
            thign.close()
    # Now glyphs[0] corresponds to ' ', glyphs[1] to '!', glyphs[2] to '"', etc.
