import React from 'react';
import { CATEGORIES } from '../constants/categories';

export default function CategoryTabs({ activeCategory, onCategoryChange }) {
    return (
        <div className="flex space-x-1 p-1 bg-surface-100 rounded-lg overflow-x-auto">
            <button
                onClick={() => onCategoryChange('all')}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${activeCategory === 'all'
                        ? 'bg-white text-primary-600 shadow-sm'
                        : 'text-gray-500 hover:text-gray-700 hover:bg-surface-200'
                    }`}
            >
                All
            </button>
            {CATEGORIES.map(cat => (
                <button
                    key={cat.id}
                    onClick={() => onCategoryChange(cat.id)}
                    className={`px-4 py-2 rounded-md text-sm font-medium whitespace-nowrap transition-all ${activeCategory === cat.id
                            ? 'bg-white text-primary-600 shadow-sm'
                            : 'text-gray-500 hover:text-gray-700 hover:bg-surface-200'
                        }`}
                >
                    {cat.label}
                </button>
            ))}
        </div>
    );
}
