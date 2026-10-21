import { signTransactionMessageWithSigners } from '@solana/kit';
import { getTransferSolInstruction } from '@solana-program/system';
import { getTransferCheckedInstruction } from '@solana-program/token';
export async function pay(message, signer, recipient, amount) {
 const sol = getTransferSolInstruction({source: signer, destination: recipient, amount});
 const token = getTransferCheckedInstruction({authority: signer, amount});
 return signTransactionMessageWithSigners(message);
}
