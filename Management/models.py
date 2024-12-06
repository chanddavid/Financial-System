from django.db import models
from Account.models import Users
from django.utils import timezone

class Income(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Received', 'Received'),
    ]
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='incomes')
    source_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_received = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.source_name} - {self.amount}"
    
    class Meta:
        db_table = 'Income'
        verbose_name = 'Income'
        verbose_name_plural =  'Incomes'
    
    



class Expense(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    ]
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.category} - {self.amount}"
    
    class Meta:
        db_table = 'Expense'
        verbose_name = 'Expense'
        verbose_name_plural =  'Expenses'
    



class Loan(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Paid', 'Paid'),
    ]
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    loan_name = models.CharField(max_length=255)
    principal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2) 
    tenure_months = models.PositiveIntegerField()
    monthly_installment = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    remaining_balance = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.loan_name} - {self.status}"

    def save(self, *args, **kwargs):
        # Calculate monthly installment using the EMI formula
        if self.principal_amount and self.interest_rate and self.tenure_months:
            r = self.interest_rate / 1200  # Monthly interest rate
            n = self.tenure_months
            emi = self.principal_amount * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)
            self.monthly_installment = round(emi, 2)
        self.remaining_balance = self.principal_amount  # Initial balance equals principal
        super().save(*args, **kwargs)


    class Meta:
        db_table = 'Loan'
        verbose_name = 'Loan'
        verbose_name_plural =  'Loans'

