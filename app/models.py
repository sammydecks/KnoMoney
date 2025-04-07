from django.db import models
from django.utils import timezone

# Create your models here
class Referral(models.Model):
    referral_id = models.AutoField(primary_key=True, serialize=True)
    email = models.EmailField(max_length=255)
    submit_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Email: {self.email} - {self.submit_time.strftime('%m-%d-%Y %H:%M:%S')}"


class LoanCalculation(models.Model):
    loancalculation_id = models.AutoField(primary_key=True, serialize=True)
    expected_grad_date = models.DateTimeField(null=False)
    submit_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{str(self.loancalculation_id)}: {self.submit_time.strftime("%m-%d-%Y %H:%M:%S")}"

class IndividualLoan(models.Model):
    loan_id = models.AutoField(primary_key=True, serialize=True)
    loancalculation = models.ForeignKey(LoanCalculation, on_delete=models.CASCADE)
    loan_num = models.IntegerField()
    principal = models.DecimalField(max_digits=10, decimal_places=2)
    interest = models.DecimalField(max_digits=5, decimal_places=2)
    loan_type = models.CharField(max_length=50)
    sem_received = models.CharField(max_length=100)

    def __str__(self):
        return f"Calculation {self.loancalculation_id}: Loan {self.loan_id} - Amount: {self.principal}"
