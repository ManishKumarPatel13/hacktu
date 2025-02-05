import numpy as np

def calculate_cibil_score_vectorized(payment_history, credit_utilization, credit_age, credit_mix, new_inquiries):
    """Vectorized CIBIL score calculator optimized for performance."""
    # Payment History Score calculation
    payment_score = np.clip(100 - 10 * payment_history, 50, 100)
    payment_score = np.where(payment_history == 0, 100, payment_score)

    # Credit Utilization Score calculation
    utilization_diff = credit_utilization - 30
    utilization_score = np.select(
        [credit_utilization <= 30, credit_utilization <= 50],
        [100, 100 - 2 * utilization_diff],
        default=50
    )

    # Credit Age Score calculation
    age_score = np.where(credit_age <= 5, 50 + 10 * credit_age, 100)

    # Credit Mix Score calculation
    mix_score = np.select(
        [credit_mix == 'mixed', credit_mix == 'unsecured'],
        [100, 80],
        default=70
    )

    # New Inquiries Score calculation
    inquiries_score = np.clip(100 - 20 * new_inquiries, 40, 100)
    inquiries_score = np.where(new_inquiries == 0, 100, inquiries_score)

    # Weighted sum calculation using matrix operations
    weighted_sum = (
        payment_score * 0.35 +
        utilization_score * 0.30 +
        age_score * 0.15 +
        mix_score * 0.10 +
        inquiries_score * 0.10
    )

    # Final score scaling with rounding
    return np.round(300 + 6 * weighted_sum).astype(np.int16)
