from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from ..models import Salesman , IncentiveDetail # import your Salesman model

@login_required(login_url='login')
def monthly_incentive_view(request):
    """
    Displays all salesmen and their total incentives for the current month/year.
    """
    now = datetime.now()
    current_month = now.strftime("%B")
    current_year = now.year

    # Get all salesmen
    salesmen = Salesman.objects.all()

    # Calculate total incentive for each salesman
    for salesman in salesmen:
        incentives = IncentiveDetail.objects.filter(
            salesman=salesman,
            month=current_month,
            year=current_year
        )

        total = 0
        for i in incentives:
            net_achieved = i.achieved - i.returns
            if net_achieved >= i.target:
                total += net_achieved * i.incentive_percent

        salesman.total_incentive = total  # dynamic attribute

    return render(request, 'monthly_incentive.html', {
        "admin_name": request.user.username,
        "current_month": current_month,
        "current_year": current_year,
        "salesmen": salesmen,
    })
@login_required(login_url='login')
def add_incentive_details_view(request, salesman_id):
    salesman = get_object_or_404(Salesman, id=salesman_id)
    now = datetime.now()
    current_month = now.strftime("%B")
    current_year = now.year

    incentives = IncentiveDetail.objects.filter(
        salesman=salesman,
        month=current_month,
        year=current_year
    ).order_by('id')

    if request.method == "POST":
        delete_id = request.POST.get("delete_id")
        if delete_id:
            IncentiveDetail.objects.filter(id=delete_id).delete()
            return redirect('add_incentive_details', salesman_id=salesman.id)

        # Process all posted rows week by week
        for key in request.POST:
            if key.startswith("route_"):
                parts = key.split("_")
                week, row_num = parts[1], parts[2]

                route = request.POST.get(f"route_{week}_{row_num}")
                id_val = request.POST.get(f"id_{week}_{row_num}")

                # Get values and remove commas
                target_val = request.POST.get(f"target_{week}_{row_num}", "0").replace(',', '')
                achieved_val = request.POST.get(f"achieved_{week}_{row_num}", "0").replace(',', '')
                returns_val = request.POST.get(f"returns_{week}_{row_num}", "0").replace(',', '')
                incentive_val = request.POST.get(f"incentive_{week}_{row_num}", "0.02").replace(',', '')

                # Convert to float
                try:
                    target = float(target_val)
                except ValueError:
                    target = 0
                try:
                    achieved = float(achieved_val)
                except ValueError:
                    achieved = 0
                try:
                    returns = float(returns_val)
                except ValueError:
                    returns = 0
                try:
                    incentive_percent = float(incentive_val)
                except ValueError:
                    incentive_percent = 0.02

                # Calculate net achieved and incentive value
                net_achieved = achieved - returns
                incentive_value = net_achieved * incentive_percent if net_achieved >= target else 0

                if route:
                    if id_val:  # Update existing
                        obj = IncentiveDetail.objects.get(id=id_val)
                        obj.route = route
                        obj.target = target
                        obj.achieved = achieved
                        obj.returns = returns
                        obj.incentive_percent = incentive_percent
                        obj.week = week
                        obj.save()
                    else:  # Create new
                        IncentiveDetail.objects.create(
                            salesman=salesman,
                            month=current_month,
                            year=current_year,
                            week=week,
                            route=route,
                            target=target,
                            achieved=achieved,
                            returns=returns,
                            incentive_percent=incentive_percent
                        )

        # Redirect after all rows processed
        return redirect('add_incentive_details', salesman_id=salesman.id)

    return render(request, 'add_incentive_details.html', {
        "admin_name": request.user.username,
        "salesman": salesman,
        "current_month": current_month,
        "current_year": current_year,
        "incentives": incentives,
    })
