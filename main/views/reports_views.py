from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
from ..models import Salesman, IncentiveDetail
import json

@login_required(login_url='login')
def reports_view(request):
    from datetime import datetime
    now = datetime.now()

    # --- Month/Year filter ---
    selected_month = request.GET.get("month", now.strftime("%B"))
    selected_year = int(request.GET.get("year", now.year))

    months = [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ]
    years = list(range(now.year-5, now.year+1))  # last 5 years till current

    # Fetch data for given month/year
    salesmen = Salesman.objects.all()
    summary_data = []
    bar_labels, bar_values = [], []
    trend_data = {}

    for salesman in salesmen:
        incentives = IncentiveDetail.objects.filter(
            salesman=salesman,
            month=selected_month,
            year=selected_year
        )

        total = 0
        for i in incentives:
            net_achieved = i.achieved - i.returns
            if net_achieved >= i.target:
                total += net_achieved * i.incentive_percent

        summary_data.append({"name": salesman.name, "total_incentive": total})
        bar_labels.append(salesman.name)
        bar_values.append(total)

        # trend chart (across weeks)
        weeks = [1, 2, 3, 4]
        week_totals = []
        for w in weeks:
            w_incentives = incentives.filter(week=w)
            w_total = 0
            for i in w_incentives:
                net_achieved = i.achieved - i.returns
                if net_achieved >= i.target:
                    w_total += net_achieved * i.incentive_percent
            week_totals.append(w_total)

        trend_data[salesman.name] = {"labels": [f"Week {w}" for w in weeks], "values": week_totals}

    return render(request, "reports.html", {
        "admin_name": request.user.username,
        "current_month": selected_month,
        "current_year": selected_year,
        "months": months,
        "years": years,
        "summary_data": summary_data,
        "bar_labels": bar_labels,
        "bar_values": bar_values,
        "trend_data": trend_data,
    })
