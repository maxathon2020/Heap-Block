from blockchain import Blockchain
import individual_person

if __name__ == '__main__':
    blockchain = Blockchain()

    me = individual_person.IndividualPerson('Patient Louis')
    nurse_1 = individual_person.IndividualPerson('Nurse GELINEAU')
    doctor_1 = individual_person.IndividualPerson('Dr. VANSTEENKISTE')
    pharmacy_1 = individual_person.IndividualPerson('Pharmacy next door')

    drug_1_data_transaction_id, drug_1_acl_transaction_id = me.add_medical_transaction(
        blockchain,
        me,
        'Louis felt dizzy. I prescribed XXXX drug.'
    )

    # me.add_medical_transaction(
    #     blockchain,
    #     doctor_1,
    #     'Louis broke one of his finger. He sould stop working for 3 days.'
    # )

    blockchain.new_block(1)

    acl_name_pharmacy = 'prescripions'
    me.add_key_to_keychain(acl_name_pharmacy, [drug_1_acl_transaction_id])
    me.share_medical_data_via_private_keys(blockchain, [acl_name_pharmacy], pharmacy_1)

    print(blockchain)
