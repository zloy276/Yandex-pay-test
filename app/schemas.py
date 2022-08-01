from marshmallow import Schema, fields


class CloudPaymentsSchema(Schema):
    """
    CloudPayments принимает поля в PascalCase
    """
    Amount = fields.Integer(required=True)
    Currency = fields.String(required=False)
    IdAddress = fields.String(required=True)
    CardCryptogramPacket = fields.String(required=True)
    Name = fields.String(required=False)
    PaymentUrl = fields.String(required=False)
    InvoiceId = fields.String(required=False)
    Description = fields.String(required=False)
    Email = fields.String(required=False)
    Payer = fields.Dict(keys=fields.Str(), values=fields.Str(), required=False)
    JsonData = fields.Dict(keys=fields.Str(), values=fields.Str(), required=False)
