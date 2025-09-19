# Script para eliminar todos los servicios de prueba
# Elimina servicios que empiezan por "test_" en organization "services"

# Script para eliminar todos los servicios de prueba
# Elimina servicios que empiezan por "test_" en organization "services"

import getpass
import time

from ndp_ep import APIClient


def get_authenticated_client():
    """Get authenticated API client."""
    API_BASE_URL = "http://localhost:8003"

    print("🔐 Authentication Required")
    api_token = getpass.getpass("Enter API Token: ")

    if not api_token.strip():
        print("❌ No token provided. Exiting.")
        return None

    try:
        client = APIClient(base_url=API_BASE_URL, token=api_token)
        print("✅ Client initialized successfully")
        return client
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return None


def find_test_services(client, prefix="test_", services_org="services"):
    """Find all test services to delete."""
    print("🔍 Searching for test services...")

    try:
        search_results = client.advanced_search(
            {"owner_org": services_org, "server": "local"}
        )
        print(
            f"📊 Found {len(search_results)} total services in '{services_org}' org"
        )

        test_services = [
            service
            for service in search_results
            if service.get("name", "").startswith(prefix + "service_")
        ]

        print(f"📊 Found {len(test_services)} test services to delete")
        return test_services

    except Exception as e:
        print(f"❌ Failed to search for services: {e}")
        return None


def show_services_to_delete(test_services):
    """Display services that will be deleted."""
    if len(test_services) == 0:
        print("✅ No test services found. Nothing to clean up!")
        return False

    print("\n📋 Services to be deleted:")
    for i, service in enumerate(test_services[:10], 1):
        name = service.get("name", "Unknown")
        service_id = service.get("id", "No ID")
        print(f"   {i:3d}. {name} (ID: {service_id})")

    if len(test_services) > 10:
        print(f"   ... and {len(test_services) - 10} more")

    return True


def get_deletion_confirmation(count):
    """Get user confirmation for deletion."""
    print(f"\n⚠️  WARNING: About to delete {count} services!")
    confirmation = input("Type 'DELETE' to proceed: ").strip()
    return confirmation == "DELETE"


def delete_services(client, test_services):
    """Delete the test services."""
    print(f"\n🗑️  Deleting {len(test_services)} test services...")
    print("=" * 40)

    deleted_count = 0
    failed_count = 0

    for i, service in enumerate(test_services, 1):
        service_name = service.get("name", f"service_{i}")

        try:
            client.delete_resource_by_name(service_name, server="local")
            deleted_count += 1
            timestamp = time.strftime("%H:%M:%S")
            print(f"✅ [{timestamp}] Deleted: {service_name}")
        except Exception as e:
            failed_count += 1
            timestamp = time.strftime("%H:%M:%S")
            print(f"❌ [{timestamp}] Failed to delete {service_name}: {e}")

        if i % 10 == 0 or i == len(test_services):
            percentage = (i / len(test_services)) * 100
            print(f"📈 Progress: {i}/{len(test_services)} ({percentage:.1f}%)")

        time.sleep(0.2)

    return deleted_count, failed_count


def print_summary(deleted_count, failed_count, total_count):
    """Print deletion summary."""
    print("\n📊 CLEANUP SUMMARY")
    print("=" * 30)
    print(f"✅ Successfully deleted: {deleted_count}")
    print(f"❌ Failed to delete: {failed_count}")
    print(f"📦 Total processed: {total_count}")

    if failed_count == 0:
        print("\n🎉 All test services cleaned up successfully!")
    else:
        print(f"\n⚠️  {failed_count} services could not be deleted")
        print("   Manual cleanup may be required")


def verify_cleanup(client, prefix="test_", services_org="services"):
    """Verify cleanup was successful."""
    print("\n🔍 Verifying cleanup...")

    try:
        verify_results = client.advanced_search(
            {
                "search_term": prefix.rstrip("_"),
                "filter_list": [f"owner_org:{services_org}"],
                "server": "local",
            }
        )

        remaining_services = [
            s
            for s in verify_results
            if s.get("name", "").startswith(prefix + "service_")
        ]

        print(f"📊 Remaining test services: {len(remaining_services)}")

        if len(remaining_services) == 0:
            print("✅ Cleanup verification: SUCCESS - No test services remain")
        else:
            print(
                f"⚠️  Cleanup verification: {len(remaining_services)}"
                " services still exist"
            )

    except Exception as e:
        print(f"❌ Verification failed: {e}")


def cleanup_test_services():
    """Clean up all test services that start with 'test_' in 'services' org."""
    PREFIX = "test_"
    SERVICES_ORG = "services"

    print("🧹 TEST SERVICES CLEANUP SCRIPT")
    print("=" * 50)
    print(f"Target: Services starting with '{PREFIX}' in '{SERVICES_ORG}' org")

    # Get authenticated client
    client = get_authenticated_client()
    if not client:
        return

    # Find test services
    test_services = find_test_services(client, PREFIX, SERVICES_ORG)
    if test_services is None:
        return

    # Show services and get confirmation
    if not show_services_to_delete(test_services):
        return

    if not get_deletion_confirmation(len(test_services)):
        print("🚫 Operation cancelled by user")
        return

    # Delete services
    deleted_count, failed_count = delete_services(client, test_services)

    # Print summary and verify
    print_summary(deleted_count, failed_count, len(test_services))
    verify_cleanup(client, PREFIX, SERVICES_ORG)


if __name__ == "__main__":
    cleanup_test_services()
