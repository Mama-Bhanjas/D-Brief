import React from 'react';
import { useWallet } from '../context/WalletContext';
import { truncateAddress } from '../utils/truncateAddress';
import { Wallet } from 'lucide-react';

export default function WalletConnect() {
    const { account, connectWallet, disconnectWallet } = useWallet();

    return (
        <div>
            {account ? (
                <div className="flex items-center space-x-3 bg-surface-100 px-4 py-2 rounded-full border border-surface-200">
                    <div className="h-2 w-2 bg-green-500 rounded-full animate-pulse"></div>
                    <span className="text-sm font-medium text-surface-700">{truncateAddress(account)}</span>
                    <button
                        onClick={disconnectWallet}
                        className="text-xs text-red-500 hover:text-red-700 font-medium ml-2"
                    >
                        Disconnect
                    </button>
                </div>
            ) : (
                <button
                    onClick={connectWallet}
                    className="flex items-center gap-2 px-6 py-2.5 text-sm font-semibold text-white bg-primary-600 rounded-full hover:bg-primary-700 transition-colors shadow-sm hover:shadow-md"
                >
                    <Wallet className="h-4 w-4" />
                    Connect Wallet
                </button>
            )}
        </div>
    );
}
