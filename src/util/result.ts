export interface Result<T> {
	error: string | null;
	success: boolean;
	value: T | null;
}
