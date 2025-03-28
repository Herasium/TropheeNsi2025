from HeraEngine.types.Texture import Texture
from HeraEngine.logger import Logger
from HeraEngine.types.Vec2 import Vec2

class Font():
    def __init__(self,name,corrupted = False):
        self._name = name
        self._corrupted = corrupted
        
        self._path = "Assets/Textures/Fonts/" + self._name

        self._charset = " !"+'"'+"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ["+"\\"+"]^_`abcdefghijklmnopqrstuvwxyz"
        self._charset_sanitized = {' ': 'space', '!': 'exclamation_mark', '"': 'double_quote', '#': 'hash', '$': 'dollar_sign', '%': 'percent', '&': 'ampersand', '\'': 'apostrophe', '(': 'left_paren', ')': 'right_paren', '*': 'asterisk', '+': 'plus', ',': 'comma', '-': 'hyphen', '.': 'period', '/': 'forward_slash', '0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', ':': 'colon', ';': 'semicolon', '<': 'less_than', '=': 'equals', '>': 'greater_than', '?': 'question_mark', '@': 'at_symbol', 'A': 'A_maj', 'B': 'B_maj', 'C': 'C_maj', 'D': 'D_maj', 'E': 'E_maj', 'F': 'F_maj', 'G': 'G_maj', 'H': 'H_maj', 'I': 'I_maj', 'J': 'J_maj', 'K': 'K_maj', 'L': 'L_maj', 'M': 'M_maj', 'N': 'N_maj', 'O': 'O_maj', 'P': 'P_maj', 'Q': 'Q_maj', 'R': 'R_maj', 'S': 'S_maj', 'T': 'T_maj', 'U': 'U_maj', 'V': 'V_maj', 'W': 'W_maj', 'X': 'X_maj', 'Y': 'Y_maj', 'Z': 'Z_maj', '[': 'left_bracket', '\\': 'backslash', ']': 'right_bracket', '^': 'caret', '_': 'underscore', '`': 'backtick', 'a': 'a_min', 'b': 'b_min', 'c': 'c_min', 'd': 'd_min', 'e': 'e_min', 'f': 'f_min', 'g': 'g_min', 'h': 'h_min', 'i': 'i_min', 'j': 'j_min', 'k': 'k_min', 'l': 'l_min', 'm': 'm_min', 'n': 'n_min', 'o': 'o_min', 'p': 'p_min', 'q': 'q_min', 'r': 'r_min', 's': 's_min', 't': 't_min', 'u': 'u_min', 'v': 'v_min', 'w': 'w_min', 'x': 'x_min', 'y': 'y_min', 'z': 'z_min', '{': 'left_brace', '|': 'vertical_bar', '}': 'right_brace', '~': 'tilde'}

        self._charset_data = {}

        self.load_charset()

        self._char_size = self._charset_data["o"].size
        self._char_offset = Vec2(0,0)
        
        if self._corrupted:
            self._name += "_corrupted"

        Logger().INFO(f"Loaded font {self._name} with {len(self._charset)} chars and a size of {self._char_size}")

    def load_charset(self):
        if self._corrupted:
            for i in self._charset:
                self._charset_data[i] = Texture(self._path + f"/{self._charset_sanitized[i]}.raw.corrupted")
        else:
            for i in self._charset:
                self._charset_data[i] = Texture(self._path + f"/{self._charset_sanitized[i]}.raw")

    @property
    def offset(self):
        return self._char_offset

    @offset.setter
    def offset(self,value):
        if not isinstance(value,Vec2):
            raise TypeError("Char offset should be a Vec2")
        
        self._char_offset = value

    @property
    def size(self):
        return self._char_size
    
    @size.setter
    def size(self,value):
        if not isinstance(value,Vec2):
            raise TypeError("Char size should be a Vec2")
        
        self._char_size = value

    
    def get_char(self,char):
        if char in self._charset_data:
            return self._charset_data[char]
        return self._charset_data["_"]