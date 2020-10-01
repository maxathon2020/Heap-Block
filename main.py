from blockchain import Blockchain
import individual_person

if __name__ == '__main__':
    blockchain = Blockchain()

    patient_1 = individual_person.IndividualPerson()
    doctor_1 = individual_person.IndividualPerson()
    data1 = 'Prescription: Medicament 1 given to patient 1, because of disease 1'
    t1 = blockchain.add_transaction(participant_a=patient_1,
                                    participant_b=doctor_1,
                                    data=data1)
    blockchain.new_block(12345)

    patient_2 = individual_person.IndividualPerson()
    doctor_2 = individual_person.IndividualPerson()
    data2 = 'Prescription: Medicament 2 given to patient 2, because of disease 2'
    t2 = blockchain.add_transaction(participant_a=patient_2,
                                    participant_b=doctor_2,
                                    data=data2)
    blockchain.new_block(123445)

    print(blockchain.chain)
