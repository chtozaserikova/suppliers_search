import { defineStore } from 'pinia';

export const useSearchStore = defineStore({
    id: 'searchStore',
    state: () => ({
        query: '',
        searchHistory: [],
    }),
    actions: {
        setQuery(query) {
            this.query = query;
            this.searchHistory.push(query); // добавляем запрос в историю
        },
        clearQuery() {
            this.query = '';
        },
        selectQuery(query) {
            this.query = query;
        },
        deleteQuery(index) {
            this.searchHistory.splice(index, 1);
        },
        clearHistory() {
            this.searchHistory = [];
        },
    },
});
