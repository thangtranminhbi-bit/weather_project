# Weather project

## Overview

Weather Data Pipeline là dự án Data Engineering được xây dựng nhằm tự động thu thập, lưu trữ, kiểm thử và chuyển đổi dữ liệu thời tiết từ OpenWeather API trên nền tảng Google Cloud Platform.

Dự án áp dụng kiến trúc ELT (Extract - Load - Transform), sử dụng BigQuery làm Data Warehouse và dbt để xây dựng các lớp dữ liệu Bronze, Silver và Gold theo kiến trúc Medallion.

Toàn bộ pipeline được tự động hóa bằng GitHub Actions.


## Architecture

OpenWeather API ->Python Extraction -> Google Cloud Storage (Raw Layer) -> BigQuery Raw Tables -> dbt Bronze Layer -> dbt Silver Layer -> dbt Gold Layer -> Analytics & Reporting


## Technology Stack

### Programming

* Python
* SQL

### Cloud

* Google Cloud Storage (GCS)
* Google BigQuery

### Data Engineering

* ELT Pipeline
* dbt
* Data Modeling
* Medallion Architecture

### Automation

* GitHub Actions

### Version Control

* Git
* GitHub

## Project Objectives

* Thu thập dữ liệu thời tiết tự động từ API.
* Lưu trữ dữ liệu thô trên Cloud Storage.
* Xây dựng Data Warehouse trên BigQuery.
* Chuyển đổi dữ liệu bằng dbt.
* Kiểm thử chất lượng dữ liệu.
* Tự động hóa toàn bộ pipeline.

## Upsert Strategy

Dự án sử dụng BigQuery MERGE để thực hiện UPSERT.

Logic:

- INSERT khi dữ liệu chưa tồn tại.
- UPDATE khi dữ liệu đã tồn tại.

Lợi ích:

- Tránh duplicate data.
- Hỗ trợ pipeline chạy nhiều lần.
- Giảm chi phí xử lý dữ liệu.

## Data Flow

### 1. Extract

Python gọi OpenWeather API để lấy dữ liệu thời tiết.

Dữ liệu được thu thập dưới định dạng JSON.

### 2. Load

Dữ liệu được lưu vào Google Cloud Storage theo cấu trúc phân vùng:

raw/

└── year=YYYY/

└── month=MM/

└── day=DD/

Sau đó dữ liệu được nạp vào BigQuery Raw Layer.


### 3. Transform

dbt được sử dụng để xây dựng các lớp dữ liệu:

#### Bronze Layer

* Chuẩn hóa dữ liệu nguồn.
* Giữ nguyên logic gần với dữ liệu gốc.

#### Silver Layer

* Làm sạch dữ liệu.
* Chuẩn hóa kiểu dữ liệu.

#### Gold Layer

* Xây dựng bảng phục vụ phân tích.
* Tổng hợp các chỉ số thời tiết.


## Data Quality Testing

Dự án sử dụng dbt Tests để kiểm tra chất lượng dữ liệu.

Các kiểm tra bao gồm:

* not_null
* unique
* accepted_values

Ví dụ:

* ID không được null.
* Các giá trị thời tiết phải nằm trong danh sách hợp lệ.

Pipeline chỉ được xem là thành công khi các bài kiểm thử dữ liệu đều vượt qua.


## Automation

Pipeline được tự động hóa bằng GitHub Actions.

Workflow thực hiện:

1. Thu thập dữ liệu từ OpenWeather API.
2. Upload dữ liệu lên Google Cloud Storage.
3. Load dữ liệu vào BigQuery.
4. Chạy dbt run.
5. Chạy dbt test.
6. Ghi log kết quả thực thi.

Workflow có thể được kích hoạt:

* Theo lịch trình (schedule).
* Khi có sự kiện push lên github repo



## Key Learnings

Thông qua dự án này, tôi đã thực hành:

* Thiết kế ELT Pipeline.
* Làm việc với REST API.
* Lưu trữ dữ liệu trên Google Cloud Storage.
* Xây dựng Data Warehouse bằng BigQuery.
* Upsert Strategy bằng BigQuery MERGE
* Chuyển đổi dữ liệu bằng dbt.
* Kiểm thử chất lượng dữ liệu.
* Tự động hóa quy trình bằng GitHub Actions.
* Quản lý mã nguồn với Git và GitHub.


## Future Improvements

* Tích hợp Airflow cho workflow orchestration.
* Xây dựng dashboard bằng Looker Studio.
* Thiết lập CI/CD nâng cao.
* Triển khai monitoring và alerting.
* Mở rộng nguồn dữ liệu thời tiết từ nhiều API khác nhau.



## Author

Tran Minh Thang

Aspiring Data Engineer

GitHub: https://github.com/thangtranminhbi-bit
