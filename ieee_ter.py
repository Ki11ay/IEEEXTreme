import struct
import math
import sys

def hex_to_float(hexVal):
    try:
        int_val = int(hexVal, 16)
        return struct.unpack('>f', struct.pack('>I', int_val))[0]
    except (ValueError, struct.error):
        return float('nan')

def float_to_hex(flt):
    try:
        return format(struct.unpack('>I', struct.pack('>f', flt))[0], '08x')
    except struct.error:
        return '7fc00000'  # NaN representation

def nand_op(v1, v2):
    try:
        int_v1 = struct.unpack('>I', struct.pack('>f', v1))[0]
        int_v2 = struct.unpack('>I', struct.pack('>f', v2))[0]
        nand_result = ~(int_v1 & int_v2) & 0xFFFFFFFF
        return struct.unpack('>f', struct.pack('>I', nand_result))[0]
    except struct.error:
        return float('nan')

def fused_multiply_add(a, b, c):
    if math.isnan(a) or math.isnan(b) or math.isnan(c):
        return float('nan')
    
    if math.isinf(a) and b == 0.0 or a == 0.0 and math.isinf(b):
        return float('nan')
    
    if math.isinf(a) and math.isinf(b):
        return float('nan')
    
    if math.isnan(a * b):
        return float('nan')
    
    if a == 0.0 or b == 0.0:
        sign_a = math.copysign(1, a)
        sign_b = math.copysign(1, b)
        if sign_a * sign_b < 0:
            return -0.0
    
    try:
        result = a * b + c
        if math.isinf(result) and not (math.isinf(a) or math.isinf(b) or math.isinf(c)):
            return float('nan')  # Handle overflow
        return result
    except OverflowError:
        return float('inf') if a * b > 0 else -float('inf')

def execute_cmd(con, lut, cmd):
    try:
        C = [con]
        for command in cmd:
            cmd_parts = command.split()
            cmd_type = cmd_parts[0]
            
            if cmd_type == 'L':
                i, j, b = map(int, cmd_parts[1:])
                if i >= len(C) or i < 0:
                    return float('nan')
                mask = int((C[i] * (1 << j)) % (1 << b))
                if i >= len(lut) or mask >= len(lut[i]):
                    return float('nan')
                C.append(lut[i][mask])
            
            elif cmd_type == 'N':
                i, j = map(int, cmd_parts[1:])
                if i >= len(C) or j >= len(C) or i < 0 or j < 0:
                    return float('nan')
                C.append(nand_op(C[i], C[j]))
            
            elif cmd_type == 'F':
                i, j, k = map(int, cmd_parts[1:])
                if i >= len(C) or j >= len(C) or k >= len(C) or i < 0 or j < 0 or k < 0:
                    return float('nan')
                C.append(fused_multiply_add(C[i], C[j], C[k]))
            
            elif cmd_type == 'C':
                try:
                    h = int(cmd_parts[1], 16)
                    C.append(hex_to_float(format(h, '08x')))
                except (ValueError, IndexError):
                    return float('nan')
            
        return C[-1] if C else float('nan')
    except Exception:
        return float('nan')

def main():
    try:
        data = sys.stdin.read().splitlines()
        T = int(data[0].strip())
        index = 1
        results = []
        
        for _ in range(T):
            try:
                con_hex = data[index].strip()
                con = hex_to_float(con_hex)
                index += 1
                
                L = int(data[index].strip())
                index += 1
                lut = []
                
                for _ in range(L):
                    line = data[index].split()
                    k = int(line[0])
                    table_values = [hex_to_float(v) for v in line[1:]]
                    if len(table_values) != 1 << k:
                        raise ValueError(f"Invalid lookup table size for k={k}")
                    lut.append(table_values)
                    index += 1
                
                Q = int(data[index].strip())
                index += 1
                cmd = data[index:index + Q]
                index += Q
                
                result = execute_cmd(con, lut, cmd)
                results.append(float_to_hex(result))
                
            except (IndexError, ValueError):
                results.append('7fc00000')
        
        for result in results:
            print(result)
            
    except Exception:
        print('7fc00000')

if __name__ == "__main__":
    main()