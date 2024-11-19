from math import log2

def calculate_probabilities():
    # Вероятности для суммы и произведения
    sum_prob = {}
    prod_prob = {}
    joint_prob = {}

    # Все возможные исходы броска двух костей
    for i in range(1, 7):
        for j in range(1, 7):
            sum_value = i + j
            prod_value = i * j

            if sum_value not in sum_prob:
                sum_prob[sum_value] = 0
            sum_prob[sum_value] += 1

            if prod_value not in prod_prob:
                prod_prob[prod_value] = 0
            prod_prob[prod_value] += 1

            if (sum_value, prod_value) not in joint_prob:
                joint_prob[(sum_value, prod_value)] = 0
            joint_prob[(sum_value, prod_value)] += 1

    total = 6 * 6

    for key in sum_prob:
        sum_prob[key] /= total
    for key in prod_prob:
        prod_prob[key] /= total
    for key in joint_prob:
        joint_prob[key] /= total

    return sum_prob, prod_prob, joint_prob

def calculate_entropy(probabilities):
    return -sum(p * log2(p) for p in probabilities.values())

def main():
    sum_prob, prod_prob, joint_prob = calculate_probabilities()

    # H(A), H(B), и H(AB)
    H_A = calculate_entropy(sum_prob)
    H_B = calculate_entropy(prod_prob)
    H_AB = calculate_entropy(joint_prob)

    # Условная энтропия H(B|A) = H(AB) - H(A)
    H_B_given_A = H_AB - H_A

    # Информация I(A;B) = H(B) - H(B|A)
    I_A_B = H_B - H_B_given_A

    return [round(H_AB, 2), round(H_A, 2), round(H_B, 2), round(H_B_given_A, 2), round(I_A_B, 2)]

# Пример использования
result = main()
print(result)

