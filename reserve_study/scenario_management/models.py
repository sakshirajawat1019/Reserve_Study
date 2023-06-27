from django.db import models
from accounts.models import CustomUser
class ScenarioManagement(models.Model):
    id = models.AutoField(primary_key=True)
    scenario_name = models.CharField(max_length=100, blank=True, default='')
    notes = models.CharField(max_length=100, blank=True, default='')
    last_saved_date	= models.DateTimeField(auto_now_add=True)
    last_saved_by = models.ForeignKey(CustomUser,null = True, on_delete=models.CASCADE, related_name="last_saved_by")
    status = models.BooleanField(default=False) 
    active = models.BooleanField(default=False)
    MonthalyCommonExpenses = models.BooleanField(default=True)  
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="created_by"),
    read_access_users = models.ManyToManyField(CustomUser, related_name='scenarios_with_read_access', blank=True)
    write_access_users = models.ManyToManyField(CustomUser, related_name='scenarios_with_write_access', blank=True)

class IntialParameters(models.Model):
    id = models.AutoField(primary_key=True)
    scenario_id = models.ForeignKey(ScenarioManagement, null=True, on_delete=models.CASCADE)
    fiscal_year_start = models.DateField(blank=False,null=False, default='2019-1-1')
    fiscal_year_end = models.DateField(blank=False, default='2019-12-31')
    starting_balance = models.FloatField(blank=False, default=40000.00)
    monthly_reserve_contribution = models.FloatField(blank=False, default=20000.00/12/30)
    current_yearly_reserve_contribution = models.FloatField(blank=False, default=20000.00)
    proposed_yearly_reserve_contribution = models.FloatField(blank=False, default=1.0)
    inflation = models.FloatField(blank=False, default=3.0)
    Number_of_units = models.IntegerField(blank=False, default=1)
    Default_interest_rate = models.FloatField(blank=False, default=0.0)
    Total_assessment_amount_per_month = models.FloatField(blank=False, default=1.00)
    minus_delinquent_payments = models.BooleanField(default=False) 
    delinquent_discount = models.FloatField(blank=False, default=0.0)

    # def save(self, *args, **kwargs):
    #     self.my_float = round(self.Default_interest_rate, 2)
    #     super(Intial_paremeters, self).save(*args, **kwargs)

class UnitsIfVariable(models.Model):
    id = models.AutoField(primary_key=True)
    scenario_id = models.ForeignKey(ScenarioManagement, null=True, on_delete=models.CASCADE)
    unit  = models.CharField(max_length=100, blank=False, null=False, default='')
    building = models.IntegerField(blank=False,null=False,  default=1)
    address = models.CharField(max_length=100, blank=False, default='New address')
    square_footage = models.FloatField(max_length=100, blank=False, default=100.00)
    percentage = models.FloatField(blank=False, null=False, default=100.00)

class SpecialAssessments(models.Model):
    id = models.AutoField(primary_key=True)
    scenario_id = models.ForeignKey(ScenarioManagement, null=True, on_delete=models.CASCADE)
    year = models.CharField(blank=False,null=False, default=2019-2020)
    amount = models.FloatField(blank=False, default=0.00)
    purpose = models.CharField(max_length=100, blank=True, default='None')

class Components(models.Model):
    id = models.AutoField(primary_key=True)
    scenario_id = models.ForeignKey(ScenarioManagement, null=True, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, blank=True, default='other')
    Component_title = models.CharField(max_length=100, blank=True, default='New Component')
    description = models.CharField(max_length=100, blank=True, default='New')
    useful_life_year = models.IntegerField(blank=False,null=False, default=0)
    remaining_useful_life_years = models.IntegerField(blank=False,null=False,default=0)
    current_replacement_cost = models.FloatField(blank=False,null=False, default=1.00)
    assessement = models.CharField(max_length=100, blank=True, default='Fixed')
    Fund_component = models.CharField(max_length=100, blank=True, default='Funded')
    Notes = models.CharField(max_length=100, blank=True, default='None')

class LoanOtherExpenditures(models.Model):
    id = models.AutoField(primary_key=True)
    scenario_id = models.ForeignKey(ScenarioManagement, null=True, on_delete=models.CASCADE)
    year_id = models.ForeignKey(IntialParameters, null=True, on_delete=models.CASCADE)
    year = models.CharField(blank=False,null=False, default=2019-2020)
    Amount_due = models.FloatField(blank=False, default=0.00)
    Description = models.CharField(blank=False, default="There are no other expenditures")
    fund_component = models.CharField(blank=False, default='Not funded')
       
class MonthalyCommonExpenses(models.Model):
    id = models.AutoField(primary_key=True)
    scenario_id = models.ForeignKey(ScenarioManagement, null=True, on_delete= models.CASCADE)
    category = models.CharField(max_length=100, blank=True, default='other')
    Component_title = models.CharField(max_length=100, blank=True, default='New Component')
    description = models.CharField(max_length=100, blank=True, default='New')
    monthly_replacement_cost = models.FloatField(blank=False,null=False, default=1.00)
    Notes = models.CharField(max_length=100, blank=True, default='None')

    class Meta:
        ordering = ['id']
        

