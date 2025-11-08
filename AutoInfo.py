import csv
import yaml
import subprocess
import os  # <-- Thêm import còn thiếu

def xulyfile():
    """
    Hàm này đọc file CSV, cập nhật file YAML và trả về
    tên tệp YAML đã điền nếu thành công, ngược lại trả về None.
    """

    # SỬA Ở ĐÂY: Đổi tên tệp từ 'Info.csv - Sheet1.csv' thành 'Info.csv'
    csv_file_name = 'Info.csv'

    yaml_template_file = 'create_ec2.yml'
    output_yaml_file = 'Create_ec2_filled.yml' # Tên tệp YAML sẽ được tạo ra

    try:
        # --- Bước 1: Đọc dữ liệu từ tệp CSV ---
        instance_data = {}
        with open(csv_file_name, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            try:
                instance_data = next(reader)
                print(f"Đã đọc dữ liệu từ CSV: {instance_data}")
            except StopIteration:
                print(f"LỖI: Tệp CSV '{csv_file_name}' trống (không có dữ liệu).")
                return None # <-- Thất bại, trả về None

        # --- Bước 2: Đọc tệp mẫu YAML (chỉ đọc, không ghi đè) ---
        playbook_data = None
        with open(yaml_template_file, 'r', encoding='utf-8') as f:
            playbook_data = yaml.safe_load(f)
            print("Đã đọc tệp mẫu YAML thành công.")
			# --- Bước 3: Cập nhật dữ liệu vào biến (trong bộ nhớ) ---
        if playbook_data and isinstance(playbook_data, list) and 'vars' in playbook_data[0]:
            vars_section = playbook_data[0]['vars']
            for key, value in instance_data.items():
                if key in vars_section:
                    vars_section[key] = value
                    print(f"  -> Đang cập nhật: {key} = {value}")
                else:
                    print(f"  (Cảnh báo: Cột '{key}' từ CSV không có trong 'vars' của YAML)")
            print("Cập nhật YAML hoàn tất.")
        else:
            print("LỖI: Không thể tìm thấy cấu trúc 'vars' trong tệp YAML.")
            return None # <-- Thất bại, trả về None

        # --- Bước 4: Ghi đối tượng Python đã cập nhật ra TỆP MỚI ---
        # (Tệp create_ec2.yml gốc không bao giờ bị ghi đè)
        with open(output_yaml_file, 'w', encoding='utf-8') as f:
            yaml.dump(playbook_data, f, sort_keys=False, default_flow_style=False)

        print(f"\n  Thành công! Tệp mới đã được tạo: {output_yaml_file}")
        return output_yaml_file # <-- Thành công, trả về tên tệp

    except FileNotFoundError as e:
        print(f"LỖI: Không tìm thấy tệp. Hãy chắc chắn tệp '{e.filename}' tồn tại.")
        return None
    except Exception as e:
        print(f"Đã xảy ra lỗi trong hàm xulyfile: {e}")
        return None
		
def main():
    print("--- Bắt đầu xử lý tệp YAML ---")

    # Chạy hàm xulyfile và lấy tên tệp output
    filled_yaml_file = xulyfile()

    print("--- Kết thúc xử lý tệp YAML ---")

    # Kiểm tra xem tệp đã được tạo thành công chưa
    if filled_yaml_file and os.path.exists(filled_yaml_file):
        print(f"\n  Thông tin tạo EC2 đã được khởi tạo: {filled_yaml_file}")
        print("  Đang thực thi Ansible Playbook...")

        try:
            # Chạy tệp ĐÃ ĐƯỢC ĐIỀN (filled_yaml_file)
            subprocess.run(["ansible-playbook", filled_yaml_file], check=True)
            print("\n  Playbook đã chạy thành công!")

        except subprocess.CalledProcessError as e:
            print(f"\n  LỖI: Ansible thất bại với mã lỗi {e.returncode}")
        except FileNotFoundError:
            print("\n LỖI: Không tìm thấy lệnh 'ansible-playbook'. Bạn đã cài Ansible chưa?")
        except Exception as e:
            print(f"\n  LỖI: Đã xảy ra lỗi khi chạy playbook: {e}")

    else:
        print(f"\n  LỖI: Tệp {filled_yaml_file} không được tạo. Vui lòng kiểm tra lỗi ở trên.")


if __name__ == "__main__":
    main()