from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from django.http import JsonResponse
from funding_plan.views import calculate_current_funding,calculate_full_funding,calculate_threshold_funding
from fpdf import FPDF
from django.http import FileResponse
from rest_framework import generics,permissions

def generate_pdf(request):

    m = 22   #Margin
    pw = 210 - 2*m    #page width: width of A4 is 210mm
    ch = 10   #cell height

    pdf = FPDF(format='letter')
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.l_margin = m
    pdf.r_margin = m
    pdf.cell(200, 10, txt="Welcome to Reserve Study!", align="C")
    # pdf.cell(300, 10, txt="Reserve Study!", align="C")
    def table_data(data, heading, d):
        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(255,255,255)
        pdf.set_fill_color(0, 51, 102)
        pdf.set_top_margin(10)
        pdf.cell(w = 0, h= 10, txt = heading, ln = 1, fill = True)

        epw = pdf.w - 2*pdf.l_margin
        col_width = epw/d
        th = pdf.font_size
        pdf.set_font("Arial","", 10)
        pdf.set_text_color(0,0,0)

        for row in data:
            for data_1 in row:
                pdf.cell( col_width, 10, str(data_1))
            pdf.ln(8)
        return "Done"
    pdf.image("/home/sakshi/reserve_copy_new/reserve_study/reports/Image.png", x = 160, w = 30, h = 26)

    pdf.set_text_color(216,109,2)
    pdf.cell(w = 0,h =10, txt="EXECUTIVE SUMMARY", ln=1)
    pdf.ln(8)

    # PROPERTY SUMMARY
    data = (
        ("ASSOCIATION NAME", "Sample Condominium Association"),
        ("LOCATION", "Seattle, WA98104"),
        ("YEAR CONSTRUCTED", 2018),
        ("NUMBER OF UNITS", 100),
        ("FINANCIAL YEAR", "2017(Januart 1, 2017 - December 31, 2017"),
        ("REPORT LEVEL", "Level 1 Full Study with site Visit")
    )
    table_data(data, "PROPERTY SUMMARY", 3)
    pdf.ln(8)

    # Reserve Fund
    data = (
        ("PROJECTED STARTING BALANCE", "$103.613"),
        ("FULL FUNDED BALANCE, IDEAL", "$163.017"),
        ("PERCENT FUNDED", "64%"),
        ("INTEREST EARNED", "1.00%"),
        ("INFLATION RATE", "3.00%"),
    )
    table_data(data, "RESERVE FUND", 2)
    pdf.ln(8)

    # RESERVE CONTRIBUTIONS
    data = (
        ("CURRENT RESERVE FUND CONTRIBUTION", "$87.753"),
        ("FULL FUNDED MAXIMUM CONTRIBUTION", "$198.866"),
        ("BASELINE FUNDING, MINIMUM CONTRIBUTION", "$100.617"),
        ("SPECIAL ASSESSMENT", "$0"),
    )
    table_data(data, "RESERVE CONTRIBUTIONS", 2)
    pdf.ln(8)

    # 2ND Page of PDF
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)

    pdf.image("/home/sakshi/reserve_copy_new/reserve_study/reports/Image.png", x = 160, w = 30, h = 26)

    pdf.set_text_color(216,109,2)
    pdf.cell(w = 0,h =10, txt="KEY INSIGHTS", ln=1)
    pdf.ln(8)
    pdf.set_text_color(0,25,51)
    pdf.set_font("Arial", "B", 25)
    pdf.cell(w = pw/3, h=10, txt="$103,613", ln=0, align= 'C')
    pdf.cell(w = pw/3, h=10, txt="$87,753", ln=0, align="C")
    pdf.cell(w = pw/3, h=10, txt="$5,102,536", ln=1, align="C")

    pdf.set_text_color(216,109,2)
    pdf.set_font("Arial", "B", 10)

    pdf.multi_cell(w = pw/3, h = 10, txt= "Reserve Account Balance",align= "C")
    pdf.line(pdf.get_y(), 84,pdf.get_y(), 54)
    print(pdf.get_x(), pdf.get_y())
    pdf.set_xy(pdf.get_x()+pw/3, pdf.get_y()-10)
    pdf.multi_cell(w = pw/3, h = 10, txt= "Annual Reserve Contribution", align="C")
    print(pdf.get_x(), pdf.get_y())
    pdf.line(pdf.get_y()+ pw/3 + 4, 84,pdf.get_y()+pw/3 + 4, 54)
    pdf.set_xy(pdf.get_x()+(2*pw/3), pdf.get_y()-10)
    pdf.multi_cell(w = pw/3, h = 10, txt= "Projected Exprenses over 30 years",align= "C")
    pdf.ln(8)

    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(216,109,2)
    pdf.cell(w = 0,h =10, txt="FULL FUNDING STRATEGY", ln=1)
    pdf.ln(8)
    pdf.image("/home/sakshi/reserve_copy_new/reserve_study/reports/plot1.png",  x = 30, w = 150, h = 80)
   
    # 3rd Page
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    
    pdf.image("/home/sakshi/reserve_copy_new/reserve_study/reports/Image.png", x = 160, w = 30, h = 26)
    pdf.set_text_color(216,109,2)
    pdf.cell(w = 0,h =10, txt="FULL FUNDING PLAN | SUMMARY", ln=1)
    pdf.ln(8)



#     cur.execute("select * from common_expenses_major")
#     result = cur.fetchall()
    
    page_width = pdf.w - 2 * pdf.l_margin

    pdf.set_font('Courier', '', 11)
    pdf.set_text_color(255, 255, 255)
    
    col_width = page_width/9
    # print(col_width)
    
    pdf.ln(0)
    
    th = pdf.font_size
    # print(th)

    txt = "Year"
    # print(txt.center(38))
    pdf.multi_cell(col_width, th, txt.center(32), fill = True)
    pdf.set_xy(pdf.get_x()+col_width, pdf.get_y()-th*5)
    txt = "Fully Funded Balance"
#     print(txt.center(32))
    pdf.multi_cell(col_width, th,txt.center(32), fill = True)
    pdf.set_xy(pdf.get_x()+col_width * 2, pdf.get_y()-th*5)
    txt = "Percentage Funded"
#     print(txt.center(38))
    pdf.multi_cell(col_width, th, txt.center(32), fill = True)
    pdf.set_xy(pdf.get_x()+col_width * 3, pdf.get_y()- th*5)
    txt = "Begining Balance"
#     print(txt.center(32))
    pdf.multi_cell(col_width, th, txt.center(32), align="C", fill = True)
    pdf.set_xy(pdf.get_x()+col_width * 4, pdf.get_y()-th*5)
    txt = "Reserve Contribution"
#     print(txt.center(32))
    pdf.multi_cell(col_width, th, txt.center(32) , align="C", fill = True)
    pdf.set_xy(pdf.get_x()+ (col_width * 5 ), pdf.get_y()-th*5)
    txt = "Special Assessment"
#     print(txt.center(32))
    pdf.multi_cell(col_width, th, txt.center(36), align="C", fill = True)
    pdf.set_xy(pdf.get_x()+col_width * 6, pdf.get_y()-th*5)
    txt = "Interest Earned"
#     print(txt.center(32))
    pdf.multi_cell(col_width, th, txt.center(32), align="C", fill = True)
    pdf.set_xy(pdf.get_x()+col_width * 7, pdf.get_y()- th*5)
    txt = "Ending Balance"
#     print(txt.center(32))
    pdf.multi_cell(col_width, th, txt.center(32), align="C", fill = True)
    txt = "Reserve Expenditure"
    pdf.multi_cell(col_width, th, txt.center(32), align="C", fill = True)
    pdf.set_xy(pdf.get_x()+col_width * 8, pdf.get_y()- th*5)
    pdf.set_text_color(0,0,0)
    
#     for row in result:
#         print(row[7])
#         pdf.cell(col_width, th, str(row[7]), align= "C")
#         pdf.cell(col_width, th, str(row[0]), align= "C")
#         pdf.cell(col_width, th, str(row[1]), align= "C")
#         pdf.cell(col_width, th, "$" + str(row[2]), align= "C")
#         pdf.cell(col_width, th, "$" + str(row[3]), align= "C")
#         pdf.cell(col_width, th, "$" + str(row[4]), align= "C")
#         pdf.cell(col_width, th, "$" + str(row[5]), align= "C")
#         pdf.cell(col_width, th, "$" + str(row[6]), align= "C")
#         pdf.ln(th)
    
#     pdf.ln(10)
    
#     pdf.set_font('Times','',10.0) 
#     pdf.cell(page_width, 0.0, '- end of report -', align='C')

#     pdf.output("flask/example.pdf", "F")

#     return send_file("example.pdf")

# @app.route("/app", methods = ["GET", "POST"])
# def first():
#     return render_template("index.html")

# @app.route("/table", methods = ["GET", "POST"])
# def table():
#     print(mydb.is_connected())
#     cur = mydb.cursor()

#     if request.method == "GET":
#         cur.execute("select * from common_expenses_major")
#         output = cur.fetchall()

#         cur.execute("select Expenses_Name, round(Price), Years from common_expenses_year")
#         output1 = cur.fetchall()

#         cur.execute("select * from replacement_reserve")
#         output2 = cur.fetchall()

#         cur.execute("select * from replacement_reserve_major")
#         output3 = cur.fetchall()  

#         return render_template("table.html", common_expenses_major = output, common_expenses_year = output1, replacement_reserve = output2, replacement_reserve_major = output3)
    
#     elif request.method == "POST":
#         start_year = int(request.form["start_year"])
#         end_year = int(request.form["end_year"])

#         cur.execute(f"select * from common_expenses_major where Years between {start_year} and {end_year}")
#         output = cur.fetchall()

#         cur.execute(f"select Expenses_Name, round(Price), Years from common_expenses_year where Years between {start_year} and {end_year}")
#         output1 = cur.fetchall()

#         cur.execute(f"select * from replacement_reserve where Years between {start_year} and {end_year}")
#         output2 = cur.fetchall()

#         cur.execute(f"select * from replacement_reserve_major where Years between {start_year} and {end_year}")
#         output3 = cur.fetchall()  

#         return render_template("table.html", common_expenses_major = output, common_expenses_year = output1, replacement_reserve = output2, replacement_reserve_major = output3)

    
    pdf.output("reserve_study_report.pdf")
    return FileResponse(open('reserve_study_report.pdf', 'rb'), as_attachment=True, content_type='application/pdf')


class PercentFunded(generics.GenericAPIView):
    #this api is used in dashboad for showing graph of Percent Funded of every year
    permission_classes = [permissions.IsAuthenticated]
    def fundingplan(self, request, scenario_id, *args, **kwargs):

        try:
            current_Funding_plan = request.data.get("current_Funding_plan")
            threshold_funding_plan = request.data.get('threshold_funding_plan')
            full_funding_plan = request.data.get('full_funding_plan')

        except :
            return Response({'error': 'Please Pass Proper Payload'}, status=status.HTTP_400_BAD_REQUEST)
        
        
#calculate_current_funding        
        cfp = calculate_current_funding(current_Funding_plan, scenario_id)

        cpf_response_data = cfp.data

        res1 = {
            'response_data': cpf_response_data
        }
        fully_funded_balance = cpf_response_data[0]["fully_funded_balance"]
        print(fully_funded_balance)
        cfp_result = []
        for item in res1['response_data']:
            cfp_result.append({"value":item['percent_funded'],
                        "category":item['year']
                        }
                        )
            
#calculate_threshold_funding
        tfp = calculate_threshold_funding(threshold_funding_plan, scenario_id)
        tfp_response_data = tfp.data

        res2 = {
            'response_data': tfp_response_data
        }
        tfp_result = []
        for item in res2['response_data']:
            tfp_result.append({"value":item['percent_funded'],
                        "category":item['year']
                        }
                        )

#calculate_full_funding
        ffp = calculate_full_funding(full_funding_plan, scenario_id)
        ffp_response_data = ffp.data


        anual_contribution = ffp_response_data[0]["reserve_contribution"]
        res3 = {
            'response_data': ffp_response_data
        }
        ffp_result = []
        for item in res3['response_data']:
            ffp_result.append({"value":item['percent_funded'],
                        "category":item['year']
                        }
                        )
            

