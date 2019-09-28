export interface Configuration {
    activity: String,
    departureLocation: String,
    schedule: String,
    maxPrice: Number,
    participants: Number
}

export interface Surprise {
    departure_schedule: String,
    departure_location: String,
    arrival_schedule: String,
    arrival_location: String,
    price: String,
    participants: Number,
    surprise_name: String,
    event_name: String,
    event_description: String
}