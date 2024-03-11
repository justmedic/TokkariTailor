# import openpyxl
# from openpyxl.utils import get_column_letter
# from django.core.mail import EmailMessage
# from django.conf import settings

# def export_order_to_excel(order):
#     wb = openpyxl.Workbook()
#     sheet = wb.active

#     headers = ['Order ID', 'User', 'Items', 'Total Cost', 'Created', 'Updated', 'Is Paid']
#     items_desc = ", ".join([str(item) for item in order.items.all()])  
#     data = [
#         order.id,
#         order.user.username,
#         items_desc,
#         order.total_cost,
#         order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
#         order.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
#         order.is_paid
#     ]

#     for col_num, header in enumerate(headers, 1):
#         sheet[get_column_letter(col_num)+'1'] = header
#         sheet.column_dimensions[get_column_letter(col_num)].width = 20

#     for col_num, cell_value in enumerate(data, 1):
#         sheet[get_column_letter(col_num)+'2'] = cell_value

#     file_path = f'order_{order.id}.xlsx'
#     wb.save(file_path)

#     return file_path

