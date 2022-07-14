export interface Meal {
    id: string;
    name: string;
    location: string;
    description: string;
    photoUrl: string;
    rating: string;
    tagIds: string[];
}

export interface User {
    id: string;
    name: string;
    suggestedMeals: {
        ids: string[];
        expiryDate: string
    }
    favouriteMeals: {
        ids: string[];
    }
}

export interface MealTag {
    id: string;
    name: string;
}