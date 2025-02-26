import locale
import random
import time
from collections import defaultdict
from enum import StrEnum, auto
import operator
from pprint import pprint


class Report:
    @staticmethod
    def format_summary_report(report: dict[str, int | float]) -> dict[str, int | float]:
        report['count'] = int(report['count'])
        return report

    @staticmethod
    def format_orders(orders: list[dict[str, str | float]]):
        for order in orders:
            order['amount'] = Money.format_money(order['amount'])
            order['status'] = order['status'].capitalize()
        return orders


class Money:
    locale.setlocale(locale.LC_ALL, 'en_GB')

    @staticmethod
    def format_money(amount: float) -> str:
        return locale.currency(amount, grouping=True)


class Statuses(StrEnum):
    COMPLETED = auto()
    Pending = auto()
    CANCELLED = auto()


def order_stream(num_orders):
    """
   A generator that yields a stream of orders.
   Each order is a dictionary with dynamic types:
     - 'order_id': str
     - 'amount': float
     - 'status': str (randomly chosen among 'completed', 'pending', 'cancelled')
   """

    for i, _ in enumerate(range(num_orders), start=1):
        order = {
            "order_id": f"ORD{i}",
            "amount": round(random.uniform(10.0, 500.0), 2),
            "status": random.choice([status.value for status in Statuses])
        }
        # print(order)
        yield order
        time.sleep(0.001)  # simulate delay


def update_summary(report: dict[str, int | float], orders: list[dict[str, str | float]]):
    """
   Updates the mutable summary report dictionary in-place.
   For each order in the list, it increments the count and adds the order's amount.
   """
    for order in orders:
        report["count"] += 1
        report["total_amount"] += order["amount"]
    report['total_amount'] = Money.format_money(round(report["total_amount"], 2))


def get_status_text(status: Statuses):
    match status:
        case Statuses.COMPLETED:
            return f'High-Value {Statuses.COMPLETED}-orders'
        case Statuses.Pending:
            return f'{Statuses.Pending}-orders'
        case Statuses.CANCELLED:
            return f'{Statuses.CANCELLED} orders'


def main() -> None:
    num_orders: int = 50
    amount_filter: float = 300
    summary_report = defaultdict(float)
    status = Statuses.COMPLETED

    filtered_orders = list((order for order in order_stream(num_orders)
                            if order["status"] == status and operator.ge(order["amount"], amount_filter)))
    update_summary(summary_report, filtered_orders)
    print(f"Summary Report for {get_status_text(status)} of {Money.format_money(amount_filter)}")
    summary_report = Report.format_summary_report(summary_report)

    for k, v in summary_report.items():
        print(f'{k}: {v}', end=', ')
    print('', sep='\n')
    pprint(Report.format_orders(filtered_orders))


if __name__ == '__main__':
    main()
