# Dispute Resolution Feature

This document outlines the implementation of the dispute resolution feature in the Certix dApp.

## Smart Contract Changes

The `ProductEscrow.sol` smart contract has been updated to include the following dispute resolution features:

- **`Disputed` state:** The `EscrowState` enum has a `Disputed` state to indicate that a dispute has been opened.
- **`openDispute` function:** Both the buyer and the seller can call this function to put the escrow into the `Disputed` state. The function takes a `reason` string as an argument, which is stored on the blockchain.
- **`submitEvidence` function:** Both the buyer and the seller can call this function to submit evidence in the form of an IPFS hash. The evidence is not stored on the blockchain, but the IPFS hash is logged in an event.
- **`EvidenceSubmitted` event:** This event is emitted when evidence is submitted.
- **`resolveDispute` function:** A dispute resolver can call this function to resolve the dispute. The function takes the NFT and funds recipients as arguments.

## Frontend Changes

The `ProductPage.tsx` file has been updated to include the following dispute resolution features:

- **"Open Dispute" button:** A button to open a dispute is visible to both the buyer and the seller when the product is in the `Shipped` state.
- **Dispute modal:** A modal opens when the "Open Dispute" button is clicked, allowing the user to enter a reason for the dispute.
- **Evidence submission form:** A form is available to both the buyer and the seller to submit evidence in the form of an IPFS hash when the sale is in the `Disputed` state.
