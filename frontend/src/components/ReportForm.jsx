import React, { useState } from 'react';
import { CATEGORIES } from '../constants/categories';
import { Send, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';

export default function ReportForm() {
    const [formData, setFormData] = useState({
        title: '',
        description: '',
        category: CATEGORIES[0].id,
        location: '',
    });
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 2000));
        console.log("Submitting report:", formData);
        setLoading(false);
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    return (
        <motion.form
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
            onSubmit={handleSubmit}
            className="space-y-6 max-w-lg bg-white p-8 rounded-2xl shadow-lg border border-gray-100"
        >
            <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1">Title</label>
                <input
                    type="text"
                    name="title"
                    value={formData.title}
                    onChange={handleChange}
                    className="block w-full rounded-lg border-gray-200 bg-gray-50 p-3 text-sm focus:border-primary-500 focus:ring-primary-500 transition-colors"
                    placeholder="What happened?"
                    required
                />
            </div>

            <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1">Category</label>
                <div className="relative">
                    <select
                        name="category"
                        value={formData.category}
                        onChange={handleChange}
                        className="block w-full rounded-lg border-gray-200 bg-gray-50 p-3 text-sm focus:border-primary-500 focus:ring-primary-500 appearance-none"
                    >
                        {CATEGORIES.map(cat => (
                            <option key={cat.id} value={cat.id}>{cat.label}</option>
                        ))}
                    </select>
                    <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-500">
                        <svg className="h-4 w-4 fill-current" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" /></svg>
                    </div>
                </div>
            </div>

            <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1">Description</label>
                <textarea
                    name="description"
                    value={formData.description}
                    onChange={handleChange}
                    className="block w-full rounded-lg border-gray-200 bg-gray-50 p-3 text-sm focus:border-primary-500 focus:ring-primary-500 transition-colors"
                    rows="4"
                    placeholder="Provide more details..."
                    required
                ></textarea>
            </div>

            <button
                type="submit"
                disabled={loading}
                className="w-full flex justify-center items-center gap-2 bg-primary-600 text-white font-semibold py-3 px-4 rounded-lg hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
                {loading ? (
                    <>
                        <Loader2 className="animate-spin h-5 w-5" />
                        <span>Submitting...</span>
                    </>
                ) : (
                    <>
                        <Send className="h-5 w-5" />
                        <span>Submit Report</span>
                    </>
                )}
            </button>
        </motion.form>
    );
}
