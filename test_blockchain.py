from blockchain import Blockchain
import individual_person


def test_blockchain():
    blockchain = Blockchain()

    patient_1 = individual_person.IndividualPerson('Patient Louis')
    nurse_1 = individual_person.IndividualPerson('Nurse GELINEAU')
    doctor_1 = individual_person.IndividualPerson('Dr. VANSTEENKISTE')

    data1 = 'Prescription: XXXXXX drug given to Louis because of flu'
    blockchain.add_transaction(participant_a=patient_1,
                               participant_b=nurse_1,
                               data=data1)
    blockchain.new_block(12345)

    data2 = 'Diagnostic: broken hip'
    blockchain.add_transaction(participant_a=patient_1,
                               participant_b=doctor_1,
                               data=data2)
    blockchain.new_block(123445)

    print(blockchain)
