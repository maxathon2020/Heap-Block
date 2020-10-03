from blockchain import Blockchain
import individual_person

if __name__ == '__main__':
    blockchain = Blockchain()

    patient_1 = individual_person.IndividualPerson('Patient Louis')
    nurse_1 = individual_person.IndividualPerson('Nurse GELINEAU')
    data1 = 'Prescription: XXXXXX drug given to Louis because of flu'
    t1 = blockchain.add_transaction(participant_a=patient_1,
                                    participant_b=nurse_1,
                                    data=data1)
    blockchain.new_block(12345)

    patient_2 = individual_person.IndividualPerson('Patient ')
    doctor_1 = individual_person.IndividualPerson('Dr. VANSTEENKISTE')
    data2 = 'Diagnostic: broken hip'
    t2 = blockchain.add_transaction(participant_a=patient_2,
                                    participant_b=doctor_1,
                                    data=data2)
    blockchain.new_block(123445)

    print(blockchain)
