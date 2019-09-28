export interface Configuration {
    activity: String,
    departureLocation: String,
    schedule: Date,
    maxPrice: Number,
    participants: Number
}

export interface Surprise {
    departure_location: String,
    arrival_schedule: Date,
    arrival_location: String,
    price: String,
    participants: Number,
    surprise_name: String,
    event_name: String,
    event_description: String
}